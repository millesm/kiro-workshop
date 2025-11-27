# Shopping Assistant Chatbot Service

A conversational AI chatbot service built with Strands Agents SDK and AWS Bedrock Nova Pro that provides shopping assistance for an e-commerce application.

## Features

- **Product Browsing**: List and search products conversationally
- **Product Details**: Get detailed information including reviews
- **Cart Management**: Add, update, and remove items from shopping cart
- **Product Recommendations**: AI-powered product suggestions
- **Multi-turn Conversations**: Maintains context across conversation
- **Session Management**: Persistent conversation history

## Architecture

The service consists of three main layers:
1. **HTTP Server Layer**: Flask-based REST API
2. **Agent Layer**: Strands Agent with Bedrock Nova Pro
3. **Tools Layer**: Custom functions for backend API integration

## Prerequisites

- Python 3.9 or higher
- AWS Account with Bedrock access
- Access to Bedrock Nova Pro model
- Running e-commerce backend API (default: http://localhost:5000)

## Installation

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r chatbot/requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials and configuration
   ```

## Configuration

### Required Environment Variables

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

### Optional Environment Variables

- `AWS_SESSION_TOKEN`: Session token for temporary credentials (optional)
- `AWS_REGION`: AWS region for Bedrock (default: us-west-2)
- `BACKEND_API_URL`: E-commerce backend API URL (default: http://localhost:5000)
- `CHATBOT_PORT`: Port for chatbot service (default: 5001)
- `SESSION_STORAGE_DIR`: Directory for session storage (default: ./sessions)
- `LOG_LEVEL`: Logging level (default: INFO)

### AWS IAM Permissions

Your AWS credentials need the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        }
    ]
}
```

### Requesting Bedrock Model Access

1. Sign in to AWS Console
2. Navigate to Amazon Bedrock
3. Go to "Model access"
4. Request access to "Nova Pro" model
5. Wait for approval (usually immediate)

## Usage

### Starting the Service

```bash
python -m chatbot
```

The service will start on the configured port (default: 5001).

### API Endpoints

#### POST /chat
Send a message to the chatbot.

**Request**:
```json
{
  "message": "Show me all products",
  "session_id": "user-123-session-456"
}
```

**Response**:
```json
{
  "response": "Here are the available products...",
  "session_id": "user-123-session-456"
}
```

**Error Response**:
```json
{
  "error": "Error message",
  "error_type": "network|api|llm|session",
  "session_id": "user-123-session-456"
}
```

#### GET /health
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "shopping-assistant-chatbot"
}
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chatbot

# Run property-based tests only
pytest -k property
```

### Project Structure

```
chatbot/
├── __init__.py          # Package initialization
├── config.py            # Configuration management
├── tools.py             # Custom tools for backend API
├── agent.py             # Agent initialization and management
├── server.py            # Flask HTTP server
├── __main__.py          # Entry point
└── requirements.txt     # Python dependencies
```

## Troubleshooting

### "You don't have access to the model"
- Ensure you've requested access to Nova Pro in Bedrock console
- Check that your AWS region supports the model

### "Missing AWS credentials"
- Verify .env file exists and contains valid credentials
- Check environment variables are loaded correctly

### "Backend API unreachable"
- Ensure the e-commerce backend is running on the configured URL
- Check BACKEND_API_URL in .env

### "Session storage errors"
- Ensure SESSION_STORAGE_DIR exists and has write permissions
- Check disk space availability

## Production Deployment

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t shopping-chatbot .
   ```

2. Run the container:
   ```bash
   docker run -p 5001:5001 \
     -e AWS_ACCESS_KEY_ID=your_key \
     -e AWS_SECRET_ACCESS_KEY=your_secret \
     shopping-chatbot
   ```

### AWS Deployment Recommendations

- Use ECS/Fargate for containerized deployment
- Store credentials in AWS Secrets Manager
- Use IAM roles instead of access keys
- Enable CloudWatch logging
- Set up Application Load Balancer
- Implement auto-scaling

## Security Considerations

- Never commit .env file to version control
- Rotate AWS credentials regularly
- Use IAM roles in production
- Implement rate limiting
- Add authentication/authorization
- Use HTTPS in production

## Performance

- Response time target: < 3 seconds
- Tool execution: < 500ms per call
- Supports concurrent requests
- Session-based conversation history

## License

[Your License Here]

## Support

For issues and questions, please contact [your contact information].
