"""Configuration module for the Shopping Assistant Chatbot Service.

This module loads and validates environment variables required for the chatbot service.
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""
    pass


class Config:
    """Configuration class for chatbot service."""
    
    def __init__(self):
        """Initialize configuration by loading and validating environment variables."""
        self._load_config()
        self._validate_config()
    
    def _load_config(self):
        """Load configuration from environment variables."""
        # AWS Credentials (Required)
        self.aws_access_key_id: Optional[str] = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key: Optional[str] = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_session_token: Optional[str] = os.getenv('AWS_SESSION_TOKEN')
        
        # AWS Region (Optional with default)
        self.aws_region: str = os.getenv('AWS_REGION', 'us-west-2')
        
        # Backend API Configuration (Optional with default)
        self.backend_api_url: str = os.getenv('BACKEND_API_URL', 'http://localhost:5000')
        
        # Chatbot Service Configuration (Optional with defaults)
        self.chatbot_port: int = int(os.getenv('CHATBOT_PORT', '5001'))
        
        # Session Storage (Optional with default)
        self.session_storage_dir: str = os.getenv('SESSION_STORAGE_DIR', './sessions')
        
        # Logging Configuration (Optional with default)
        self.log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    
    def _validate_config(self):
        """Validate that required configuration is present.
        
        Raises:
            ConfigurationError: If required configuration is missing.
        """
        missing_configs = []
        
        # Check required AWS credentials
        if not self.aws_access_key_id:
            missing_configs.append('AWS_ACCESS_KEY_ID')
        
        if not self.aws_secret_access_key:
            missing_configs.append('AWS_SECRET_ACCESS_KEY')
        
        if missing_configs:
            error_msg = (
                f"Missing required configuration: {', '.join(missing_configs)}. "
                f"Please set these environment variables or add them to your .env file."
            )
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        
        # Log successful configuration
        logger.info("Configuration loaded successfully")
        logger.info(f"AWS Region: {self.aws_region}")
        logger.info(f"Backend API URL: {self.backend_api_url}")
        logger.info(f"Chatbot Port: {self.chatbot_port}")
        logger.info(f"Session Storage Directory: {self.session_storage_dir}")
    
    def get_aws_credentials(self) -> dict:
        """Get AWS credentials as a dictionary.
        
        Returns:
            Dictionary containing AWS credentials.
        """
        credentials = {
            'aws_access_key_id': self.aws_access_key_id,
            'aws_secret_access_key': self.aws_secret_access_key,
            'region_name': self.aws_region
        }
        
        # Add session token if provided
        if self.aws_session_token:
            credentials['aws_session_token'] = self.aws_session_token
        
        return credentials


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance.
    
    Returns:
        Config: The global configuration instance.
    
    Raises:
        ConfigurationError: If configuration cannot be loaded or validated.
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reset_config():
    """Reset the global configuration instance (useful for testing)."""
    global _config
    _config = None
