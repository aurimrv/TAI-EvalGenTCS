"""
LLM Client - Handles communication with OpenRouter API.
Implements rate limiting and retry logic.
"""

import time
import json
import re
from typing import Dict, Optional
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for API requests."""
    
    def __init__(self, requests_per_minute: int):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute
        """
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time = 0
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_interval:
            sleep_time = self.min_interval - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


class LLMClient:
    """Client for interacting with LLM via OpenRouter API."""
    
    def __init__(self, settings):
        """
        Initialize LLM client.
        
        Args:
            settings: Settings object with configuration
        """
        self.settings = settings
        
        # Initialize OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_api_base
        )
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            settings.rate_limit_requests_per_minute
        )
        
        logger.info(f"LLM Client initialized with model: {settings.llm_model}")
    
    def generate_completion(
        self,
        system_prompt: str,
        user_message: str,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Generate completion from LLM.
        
        Args:
            system_prompt: System prompt defining behavior
            user_message: User message with the task
            response_format: Optional JSON schema for structured output
        
        Returns:
            LLM response as string
        
        Raises:
            Exception: If all retry attempts fail
        """
        retry_config = self.settings.get_retry_config()
        
        for attempt in range(retry_config['attempts']):
            try:
                # Wait if needed for rate limiting
                self.rate_limiter.wait_if_needed()
                
                logger.debug(f"Sending request to LLM (attempt {attempt + 1})")
                
                # Prepare messages
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
                
                # Prepare request parameters
                request_params = {
                    "model": self.settings.llm_model,
                    "messages": messages,
                    "temperature": self.settings.llm_temperature,
                    "max_tokens": self.settings.llm_max_tokens,
                }
                
                # Add response format if provided
                # Note: Some models don't support strict JSON schema mode
                if response_format:
                    try:
                        request_params["response_format"] = {
                            "type": "json_schema",
                            "json_schema": response_format
                        }
                    except Exception as e:
                        logger.warning(f"Model may not support strict JSON schema mode: {e}")
                        # Fallback to basic JSON mode
                        request_params["response_format"] = {"type": "json_object"}
                
                # Make API call
                response = self.client.chat.completions.create(**request_params)
                
                # Extract content
                content = response.choices[0].message.content
                
                logger.debug(f"Received response from LLM ({len(content)} chars)")
                
                return content
                
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1} failed: {str(e)}"
                )
                
                if attempt < retry_config['attempts'] - 1:
                    # Calculate backoff delay
                    delay = retry_config['delay'] * (
                        retry_config['backoff_factor'] ** attempt
                    )
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("All retry attempts failed")
                    raise
    
    def generate_json_completion(
        self,
        system_prompt: str,
        user_message: str,
        json_schema: Optional[Dict] = None
    ) -> Dict:
        """
        Generate JSON completion from LLM with robust parsing.
        
        Args:
            system_prompt: System prompt defining behavior
            user_message: User message with the task
            json_schema: Optional JSON schema for validation
        
        Returns:
            Parsed JSON response as dictionary
        
        Raises:
            json.JSONDecodeError: If response cannot be parsed as valid JSON
        """
        # Request JSON format in system prompt
        enhanced_system_prompt = system_prompt + "\n\nYou MUST respond with valid JSON only."
        
        response = self.generate_completion(
            system_prompt=enhanced_system_prompt,
            user_message=user_message,
            response_format=json_schema
        )
        
        # Sanitize and parse JSON
        try:
            # Remove code block delimiters if present (```json ... ```)
            cleaned_response = self._sanitize_json_response(response)
            
            # Parse JSON
            return json.loads(cleaned_response)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content (first 500 chars): {response[:500]}")
            logger.debug(f"Response content (last 500 chars): {response[-500:]}")
            
            # Try to extract JSON from the response
            extracted_json = self._extract_json_from_text(response)
            if extracted_json:
                logger.info("Successfully extracted JSON from malformed response")
                return json.loads(extracted_json)
            
            # If all else fails, raise the original error
            raise
    
    def _sanitize_json_response(self, response: str) -> str:
        """
        Sanitize LLM response by removing code block delimiters.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Cleaned response
        """
        # Remove code block delimiters (```json ... ``` or ``` ... ```)
        cleaned = response.strip()
        
        # Remove leading code block marker
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]  # Remove ```json
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]   # Remove ```
        
        # Remove trailing code block marker
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]  # Remove ```
        
        return cleaned.strip()
    
    def _extract_json_from_text(self, text: str) -> Optional[str]:
        """
        Attempt to extract JSON object from text that may contain other content.
        
        Args:
            text: Text that may contain JSON
        
        Returns:
            Extracted JSON string or None
        """
        try:
            # Try to find JSON object by looking for balanced braces
            brace_count = 0
            start_index = -1
            
            for i, char in enumerate(text):
                if char == '{':
                    if brace_count == 0:
                        start_index = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_index != -1:
                        # Found a complete JSON object
                        potential_json = text[start_index:i+1]
                        # Validate it's actually JSON
                        try:
                            json.loads(potential_json)
                            return potential_json
                        except json.JSONDecodeError:
                            # Continue searching
                            start_index = -1
            
            return None
            
        except Exception as e:
            logger.debug(f"Failed to extract JSON from text: {e}")
            return None
    
    def __repr__(self) -> str:
        return f"LLMClient(model={self.settings.llm_model})"
