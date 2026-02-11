"""
LLM Client - Handles communication with OpenRouter API.
Implements rate limiting and retry logic.
"""

import time
import json
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
                if response_format:
                    request_params["response_format"] = {
                        "type": "json_schema",
                        "json_schema": response_format
                    }
                
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
        Generate JSON completion from LLM.
        
        Args:
            system_prompt: System prompt defining behavior
            user_message: User message with the task
            json_schema: Optional JSON schema for validation
        
        Returns:
            Parsed JSON response as dictionary
        
        Raises:
            json.JSONDecodeError: If response is not valid JSON
        """
        # Request JSON format in system prompt
        enhanced_system_prompt = system_prompt + "\n\nYou MUST respond with valid JSON only."
        
        response = self.generate_completion(
            system_prompt=enhanced_system_prompt,
            user_message=user_message,
            response_format=json_schema
        )
        
        # Parse JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {response}")
            raise
    
    def __repr__(self) -> str:
        return f"LLMClient(model={self.settings.llm_model})"
