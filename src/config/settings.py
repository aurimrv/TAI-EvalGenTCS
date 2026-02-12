"""
Configuration settings for TAI-EvalGenTCS CLI.
Loads configuration from environment variables and .env file.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize settings.
        
        Args:
            config_path: Optional path to custom .env file
        """
        # Load environment variables
        if config_path:
            load_dotenv(config_path)
        else:
            # Try to load from default locations
            env_path = Path(__file__).parent.parent.parent / '.env'
            if env_path.exists():
                load_dotenv(env_path)
        
        # OpenRouter API Configuration
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.openrouter_api_base = os.getenv(
            'OPENROUTER_API_BASE',
            'https://openrouter.ai/api/v1'
        )
        
        # LLM Configuration
        self.llm_model = os.getenv('LLM_MODEL', 'openai/gpt-4.1-mini')
        self.llm_temperature = float(os.getenv('LLM_TEMPERATURE', '0.0'))  # 0.0 for maximum determinism
        self.llm_max_tokens = int(os.getenv('LLM_MAX_TOKENS', '16000'))
        self.llm_timeout = int(os.getenv('LLM_TIMEOUT', '300'))  # 5 minutes default
        self.llm_seed = os.getenv('LLM_SEED', None)  # Seed for deterministic sampling
        if self.llm_seed is not None:
            self.llm_seed = int(self.llm_seed)        
        # Rate Limiting Configuration
        self.rate_limit_requests_per_minute = int(
            os.getenv('RATE_LIMIT_REQUESTS_PER_MINUTE', '60')
        )
        self.rate_limit_tokens_per_minute = int(
            os.getenv('RATE_LIMIT_TOKENS_PER_MINUTE', '100000')
        )
        
        # Retry Configuration
        self.retry_attempts = int(os.getenv('RETRY_ATTEMPTS', '3'))
        self.retry_delay = float(os.getenv('RETRY_DELAY', '2.0'))
        self.backoff_factor = float(os.getenv('BACKOFF_FACTOR', '3.0'))
        
        # Application Configuration
        self.app_name = os.getenv('APP_NAME', 'TAI-EvalGenTCS')
        self.app_version = os.getenv('APP_VERSION', '1.0.0')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # Paths
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / 'data'
        self.best_practices_path = self.data_dir / 'best_practices.json'
        
        # Validate paths
        if not self.best_practices_path.exists():
            raise FileNotFoundError(
                f"Best practices file not found: {self.best_practices_path}"
            )
    
    def get_openrouter_config(self) -> dict:
        """Get OpenRouter API configuration as dictionary."""
        return {
            'api_key': self.openrouter_api_key,
            'api_base': self.openrouter_api_base,
            'model': self.llm_model,
            'temperature': self.llm_temperature,
            'max_tokens': self.llm_max_tokens,
        }
    
    def get_rate_limit_config(self) -> dict:
        """Get rate limiting configuration as dictionary."""
        return {
            'requests_per_minute': self.rate_limit_requests_per_minute,
            'tokens_per_minute': self.rate_limit_tokens_per_minute,
        }
    
    def get_retry_config(self) -> dict:
        """Get retry configuration as dictionary."""
        return {
            'attempts': self.retry_attempts,
            'delay': self.retry_delay,
            'backoff_factor': self.backoff_factor,
        }
    
    def __repr__(self) -> str:
        """String representation of settings (hiding sensitive data)."""
        return (
            f"Settings(model={self.llm_model}, "
            f"api_base={self.openrouter_api_base}, "
            f"rate_limit={self.rate_limit_requests_per_minute} req/min)"
        )
