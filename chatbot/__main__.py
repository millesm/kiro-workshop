"""Main entry point for the Shopping Assistant Chatbot Service.

This module starts the chatbot service by loading configuration,
initializing the agent, and starting the HTTP server.
"""

import sys
import logging
import signal
from chatbot.config import get_config, ConfigurationError
from chatbot.server import run_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('chatbot.log')
    ]
)

logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully.
    
    Args:
        sig: Signal number
        frame: Current stack frame
    """
    logger.info("Shutdown signal received. Stopping chatbot service...")
    sys.exit(0)


def main():
    """Main function to start the chatbot service."""
    try:
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("=" * 60)
        logger.info("Shopping Assistant Chatbot Service")
        logger.info("=" * 60)
        
        # Load and validate configuration
        logger.info("Loading configuration...")
        config = get_config()
        
        # Update logging level from config
        log_level = getattr(logging, config.log_level.upper(), logging.INFO)
        logging.getLogger().setLevel(log_level)
        
        logger.info("Configuration loaded successfully")
        logger.info(f"AWS Region: {config.aws_region}")
        logger.info(f"Backend API: {config.backend_api_url}")
        logger.info(f"Chatbot Port: {config.chatbot_port}")
        logger.info(f"Session Storage: {config.session_storage_dir}")
        logger.info(f"Log Level: {config.log_level}")
        
        # Start the HTTP server
        logger.info("Starting HTTP server...")
        run_server()
    
    except ConfigurationError as e:
        logger.error("=" * 60)
        logger.error("CONFIGURATION ERROR")
        logger.error("=" * 60)
        logger.error(str(e))
        logger.error("")
        logger.error("Please ensure all required environment variables are set.")
        logger.error("See .env.example for required configuration.")
        logger.error("=" * 60)
        sys.exit(1)
    
    except Exception as e:
        logger.error("=" * 60)
        logger.error("FATAL ERROR")
        logger.error("=" * 60)
        logger.error(f"Failed to start chatbot service: {str(e)}", exc_info=True)
        logger.error("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()
