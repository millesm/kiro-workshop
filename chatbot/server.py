"""HTTP server module for the Shopping Assistant Chatbot.

This module provides a Flask-based REST API for the chatbot service.
"""

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.config import get_config
from chatbot.agent import process_message, get_active_sessions

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create and configure the Flask application.
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Configure CORS to allow requests from frontend
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint.
        
        Returns:
            JSON response indicating service health
        """
        return jsonify({
            'status': 'healthy',
            'service': 'shopping-assistant-chatbot',
            'active_sessions': get_active_sessions()
        }), 200
    
    @app.route('/chat', methods=['POST'])
    def chat():
        """Main chat endpoint for processing user messages.
        
        Expected JSON body:
            {
                "message": "user message",
                "session_id": "unique-session-id"
            }
        
        Returns:
            JSON response with chatbot reply or error
        """
        try:
            # Validate request content type
            if not request.is_json:
                logger.warning("Request received with non-JSON content type")
                return jsonify({
                    'error': 'Content-Type must be application/json',
                    'error_type': 'validation'
                }), 400
            
            # Get request data
            data = request.get_json()
            
            # Validate required fields
            if not data:
                logger.warning("Empty request body received")
                return jsonify({
                    'error': 'Request body is required',
                    'error_type': 'validation'
                }), 400
            
            message = data.get('message')
            session_id = data.get('session_id')
            
            if not message:
                logger.warning("Request missing 'message' field")
                return jsonify({
                    'error': 'Message is required',
                    'error_type': 'validation',
                    'session_id': session_id
                }), 400
            
            if not session_id:
                logger.warning("Request missing 'session_id' field")
                return jsonify({
                    'error': 'Session ID is required',
                    'error_type': 'validation'
                }), 400
            
            # Validate message length
            if len(message) > 10000:
                logger.warning(f"Message too long: {len(message)} characters")
                return jsonify({
                    'error': 'Message is too long (max 10000 characters)',
                    'error_type': 'validation',
                    'session_id': session_id
                }), 400
            
            # Log request
            logger.info(f"Chat request - Session: {session_id}, Message length: {len(message)}")
            
            # Process message with agent
            response = process_message(message, session_id)
            
            # Return response
            return jsonify({
                'response': response,
                'session_id': session_id
            }), 200
        
        except Exception as e:
            # Log error
            logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
            
            # Return error response
            session_id = data.get('session_id') if data else None
            return jsonify({
                'error': 'An internal error occurred. Please try again.',
                'error_type': 'server',
                'session_id': session_id
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors.
        
        Returns:
            JSON error response
        """
        return jsonify({
            'error': 'Endpoint not found',
            'error_type': 'not_found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors.
        
        Returns:
            JSON error response
        """
        logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'error_type': 'server'
        }), 500
    
    return app


def run_server():
    """Run the Flask server.
    
    This function starts the HTTP server on the configured port.
    """
    config = get_config()
    app = create_app()
    
    logger.info(f"Starting chatbot service on port {config.chatbot_port}")
    logger.info(f"Backend API URL: {config.backend_api_url}")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=config.chatbot_port,
        debug=False,
        threaded=True
    )
