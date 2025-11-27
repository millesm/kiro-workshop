# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create chatbot service directory structure (chatbot/, chatbot/tools.py, chatbot/agent.py, chatbot/server.py, chatbot/config.py)
  - Create requirements.txt with dependencies (strands-agents, flask, python-dotenv, requests, boto3, hypothesis)
  - Create .env.example file with required environment variables
  - Create README.md with setup and usage instructions
  - _Requirements: 10.1, 10.2_

- [x] 2. Implement configuration module
  - Create config.py to load environment variables
  - Implement validation for required AWS credentials
  - Implement default values for optional configuration
  - Add configuration error handling with clear messages
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 11.5_

- [ ]* 2.1 Write property test for configuration validation
  - **Property 7: Configuration validation at startup**
  - **Validates: Requirements 2.4, 11.5**

- [x] 3. Implement custom tools module
  - Create tools.py with tool decorator imports
  - Implement list_products() tool with backend API call
  - Implement get_product_details(product_id) tool
  - Implement get_cart() tool
  - Implement add_to_cart(product_id, quantity) tool
  - Implement update_cart_item(cart_item_id, quantity) tool
  - Implement remove_from_cart(cart_item_id) tool
  - Add error handling for all API calls with structured error returns
  - Add logging for tool invocations and errors
  - _Requirements: 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2, 7.1, 7.2, 9.1, 9.2, 11.1_

- [ ]* 3.1 Write property test for tool API calls
  - **Property 3: Tool API calls match specification**
  - **Validates: Requirements 3.2, 4.2, 5.2, 6.2, 7.2, 9.2**

- [ ]* 3.2 Write property test for tool data flow
  - **Property 4: Tool data flow completeness**
  - **Validates: Requirements 3.3, 4.3, 5.3, 6.3, 7.3, 9.3**

- [ ]* 3.3 Write property test for error handling
  - **Property 6: Comprehensive error handling**
  - **Validates: Requirements 1.5, 3.5, 11.1, 11.2, 11.3, 11.4**

- [x] 4. Implement agent module
  - Create agent.py with Strands Agent imports
  - Implement create_agent() function to initialize BedrockModel with Nova Pro
  - Configure agent with system prompt defining chatbot personality
  - Register all custom tools with the agent
  - Implement session management using FileSessionManager
  - Implement get_or_create_session(session_id) function
  - Implement process_message(message, session_id) function
  - Add error handling for LLM failures
  - Add logging for agent initialization and message processing
  - _Requirements: 1.2, 10.3, 12.1, 12.3, 12.5, 11.4_

- [ ]* 4.1 Write property test for tool invocation
  - **Property 2: Tool invocation for shopping operations**
  - **Validates: Requirements 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1**

- [ ]* 4.2 Write property test for response data inclusion
  - **Property 5: Response contains tool data**
  - **Validates: Requirements 3.4, 4.4, 5.4, 6.4, 7.4, 9.4**

- [ ]* 4.3 Write property test for recommendation validity
  - **Property 8: Recommendation product validity**
  - **Validates: Requirements 8.3**

- [ ]* 4.4 Write property test for session persistence
  - **Property 9: Session conversation persistence**
  - **Validates: Requirements 12.1, 12.3**

- [ ]* 4.5 Write property test for session isolation
  - **Property 10: Session isolation**
  - **Validates: Requirements 12.5**

- [x] 5. Implement HTTP server module
  - Create server.py with Flask application setup
  - Configure CORS to allow frontend origin
  - Implement POST /chat endpoint
  - Add request validation for message and session_id
  - Integrate with agent module for message processing
  - Implement error response formatting
  - Add logging for all requests and responses
  - Implement health check endpoint GET /health
  - _Requirements: 1.1, 1.3, 1.4, 11.3_

- [ ]* 5.1 Write property test for message processing
  - **Property 1: Message processing returns response**
  - **Validates: Requirements 1.2, 1.3**

- [x] 6. Create main entry point
  - Create main.py or __main__.py to start the service
  - Load configuration and validate at startup
  - Initialize agent with tools
  - Start HTTP server on configured port
  - Add graceful shutdown handling
  - _Requirements: 1.4, 2.1, 2.2, 2.3, 2.4_

- [x] 7. Update frontend chatbot component
  - Update Chatbot.js to send requests to chatbot service endpoint
  - Implement session ID generation and management
  - Update message handling to use new API format
  - Add error handling for chatbot service errors
  - Update UI to show loading states during API calls
  - _Requirements: 1.1, 1.3, 1.5_

- [x] 8. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Create deployment documentation
  - Document environment variable requirements
  - Document AWS IAM permissions needed
  - Create Docker configuration files (Dockerfile, docker-compose.yml)
  - Document deployment steps for local and production environments
  - Add troubleshooting guide for common issues
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 10. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
