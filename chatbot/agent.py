"""Agent module for the Shopping Assistant Chatbot.

This module manages the Strands Agent lifecycle, conversation context, and session management.
"""

import logging
import os
import boto3
from typing import Dict, Optional
from datetime import datetime
from strands import Agent
from strands.models import BedrockModel
from strands.session.file_session_manager import FileSessionManager
from chatbot.config import get_config
from chatbot.tools import ALL_TOOLS

logger = logging.getLogger(__name__)

# System prompt defining the chatbot's personality and capabilities
SYSTEM_PROMPT = """You are a helpful shopping assistant for an e-commerce store. Your role is to help customers:

1. Browse and discover products in our catalog
2. Get detailed information about products including reviews
3. Manage their shopping cart (add, update, remove items)
4. Receive personalized product recommendations

Guidelines:
- Be friendly, concise, and helpful
- When showing products, include the emoji, name, and price
- When recommending products, explain why they might be a good fit
- If a customer asks about a product not in the catalog, politely let them know it's not available
- Always confirm actions like adding to cart or removing items
- If you encounter an error, apologize and suggest an alternative action

You have access to tools that let you:
- list_products: Get all available products
- get_product_details: Get detailed info about a specific product
- get_cart: View the customer's current cart
- add_to_cart: Add items to the cart
- update_cart_item: Change quantities in the cart
- remove_from_cart: Remove items from the cart

Use these tools to help customers accomplish their shopping goals."""


# Global session storage
_sessions: Dict[str, Dict] = {}


def create_agent(session_id: str) -> Agent:
    """Create and configure a Strands Agent with Bedrock Nova Pro.
    
    Args:
        session_id: Unique identifier for the conversation session
    
    Returns:
        Configured Agent instance
    
    Raises:
        Exception: If agent creation fails
    """
    try:
        config = get_config()
        
        # Create boto3 session with credentials
        boto_session = boto3.Session(
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            aws_session_token=config.aws_session_token,
            region_name=config.aws_region
        )
        
        # Create Bedrock model
        logger.info(f"Initializing Bedrock Nova Pro model in region {config.aws_region}")
        bedrock_model = BedrockModel(
            model_id="us.amazon.nova-pro-v1:0",
            boto_session=boto_session,
            temperature=0.7,
            streaming=True
        )
        
        # Ensure session storage directory exists
        os.makedirs(config.session_storage_dir, exist_ok=True)
        
        # Create session manager
        session_manager = FileSessionManager(
            session_id=session_id,
            storage_dir=config.session_storage_dir
        )
        
        # Create agent with model, tools, and session management
        logger.info(f"Creating agent for session {session_id}")
        agent = Agent(
            model=bedrock_model,
            tools=ALL_TOOLS,
            system_prompt=SYSTEM_PROMPT,
            session_manager=session_manager,
            name="ShoppingAssistant"
        )
        
        logger.info(f"Agent created successfully for session {session_id}")
        return agent
    
    except Exception as e:
        logger.error(f"Failed to create agent: {str(e)}", exc_info=True)
        raise


def get_or_create_session(session_id: str) -> Dict:
    """Get an existing session or create a new one.
    
    Args:
        session_id: Unique identifier for the conversation session
    
    Returns:
        Dictionary containing session data including the agent
    """
    global _sessions
    
    if session_id not in _sessions:
        logger.info(f"Creating new session: {session_id}")
        
        # Create new agent for this session
        agent = create_agent(session_id)
        
        # Store session data
        _sessions[session_id] = {
            'session_id': session_id,
            'agent': agent,
            'created_at': datetime.now(),
            'last_accessed': datetime.now()
        }
    else:
        # Update last accessed time
        _sessions[session_id]['last_accessed'] = datetime.now()
        logger.info(f"Using existing session: {session_id}")
    
    return _sessions[session_id]


def process_message(message: str, session_id: str) -> str:
    """Process a user message and return the agent's response.
    
    Args:
        message: The user's message
        session_id: Unique identifier for the conversation session
    
    Returns:
        The agent's response as a string
    
    Raises:
        Exception: If message processing fails
    """
    try:
        logger.info(f"Processing message for session {session_id}: {message[:100]}...")
        
        # Get or create session
        session = get_or_create_session(session_id)
        agent = session['agent']
        
        # Process message with agent
        result = agent(message)
        
        # Extract response text
        if hasattr(result, 'content'):
            # Handle AgentResult object
            response = result.content
        elif isinstance(result, str):
            response = result
        else:
            response = str(result)
        
        logger.info(f"Generated response for session {session_id}: {response[:100]}...")
        return response
    
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        # Return user-friendly error message
        return (
            "I apologize, but I encountered an error while processing your request. "
            "Please try again or rephrase your question."
        )


def clear_session(session_id: str) -> bool:
    """Clear a session from memory.
    
    Args:
        session_id: Unique identifier for the conversation session
    
    Returns:
        True if session was cleared, False if session didn't exist
    """
    global _sessions
    
    if session_id in _sessions:
        logger.info(f"Clearing session: {session_id}")
        del _sessions[session_id]
        return True
    
    return False


def get_active_sessions() -> int:
    """Get the number of active sessions.
    
    Returns:
        Number of active sessions
    """
    return len(_sessions)
