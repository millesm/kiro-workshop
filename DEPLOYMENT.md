# Deployment Guide - Shopping Assistant Chatbot Service

This guide provides detailed instructions for deploying the Shopping Assistant Chatbot Service in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Variables](#environment-variables)
3. [AWS IAM Permissions](#aws-iam-permissions)
4. [Local Development Deployment](#local-development-deployment)
5. [Docker Deployment](#docker-deployment)
6. [AWS Production Deployment](#aws-production-deployment)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.9+**: For running the chatbot service
- **Node.js 16+**: For the frontend application
- **AWS Account**: With access to Amazon Bedrock
- **Docker** (optional): For containerized deployment

### AWS Bedrock Access

1. Sign in to AWS Console
2. Navigate to Amazon Bedrock service
3. Go to "Model access" in the left sidebar
4. Click "Manage model access"
5. Select "Nova Pro" model
6. Click "Request model access"
7. Accept terms and conditions
8. Wait for approval (usually immediate)

## Environment Variables

### Required Variables

```bash
# AWS Credentials (Required)
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
```

### Optional Variables

```bash
# AWS Session Token (for temporary credentials)
AWS_SESSION_TOKEN=your_session_token_here

# AWS Region (default: us-west-2)
AWS_REGION=us-west-2

# Backend API URL (default: http://localhost:5000)
BACKEND_API_URL=http://localhost:5000

# Chatbot Service Port (default: 5001)
CHATBOT_PORT=5001

# Session Storage Directory (default: ./sessions)
SESSION_STORAGE_DIR=./sessions

# Logging Level (default: INFO)
LOG_LEVEL=INFO
```

## AWS IAM Permissions

### Required IAM Policy

Your AWS credentials need the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/amazon.nova-pro-v1:0",
                "arn:aws:bedrock:us-west-2::foundation-model/*"
            ]
        }
    ]
}
```

### Creating IAM User (Development)

1. Go to IAM Console
2. Click "Users" → "Add users"
3. Enter username (e.g., `chatbot-service-dev`)
4. Select "Programmatic access"
5. Click "Next: Permissions"
6. Click "Attach policies directly"
7. Click "Create policy" and paste the JSON above
8. Attach the policy to the user
9. Save the Access Key ID and Secret Access Key

### Using IAM Roles (Production - Recommended)

For production deployments on AWS (EC2, ECS, Lambda), use IAM roles instead of access keys:

1. Create an IAM role with the policy above
2. Attach the role to your compute resource
3. Remove `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` from environment variables
4. The AWS SDK will automatically use the role credentials

## Local Development Deployment

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd /path/to/project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r chatbot/requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

### Step 3: Initialize Database

```bash
# Initialize the e-commerce database
npm run init-db
```

### Step 4: Start Services

```bash
# Terminal 1: Start backend API
npm run server

# Terminal 2: Start chatbot service
python -m chatbot

# Terminal 3: Start frontend
npm run client
```

### Step 5: Verify Deployment

- Backend API: http://localhost:5000/api/products
- Chatbot Service: http://localhost:5001/health
- Frontend: http://localhost:3000

## Docker Deployment

### Step 1: Build Images

```bash
# Build chatbot service image
docker build -t shopping-chatbot:latest .

# Or build all services with docker-compose
docker-compose build
```

### Step 2: Configure Environment

```bash
# Create .env file for docker-compose
cat > .env << EOF
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-west-2
LOG_LEVEL=INFO
EOF
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f chatbot

# Check status
docker-compose ps
```

### Step 4: Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## AWS Production Deployment

### Option 1: AWS ECS/Fargate

#### Prerequisites
- AWS CLI configured
- ECS cluster created
- ECR repository for Docker images

#### Steps

1. **Push Docker Image to ECR**

```bash
# Login to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

# Tag image
docker tag shopping-chatbot:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/shopping-chatbot:latest

# Push image
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/shopping-chatbot:latest
```

2. **Create Task Definition**

```json
{
  "family": "shopping-chatbot",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<account-id>:role/chatbot-task-role",
  "containerDefinitions": [
    {
      "name": "chatbot",
      "image": "<account-id>.dkr.ecr.us-west-2.amazonaws.com/shopping-chatbot:latest",
      "portMappings": [
        {
          "containerPort": 5001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AWS_REGION",
          "value": "us-west-2"
        },
        {
          "name": "BACKEND_API_URL",
          "value": "http://backend-service:5000"
        },
        {
          "name": "LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/shopping-chatbot",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

3. **Create ECS Service**

```bash
aws ecs create-service \
  --cluster my-cluster \
  --service-name shopping-chatbot \
  --task-definition shopping-chatbot \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Option 2: AWS EC2

1. **Launch EC2 Instance**
   - AMI: Amazon Linux 2 or Ubuntu
   - Instance Type: t3.medium or larger
   - Security Group: Allow ports 5001 (chatbot), 5000 (backend), 3000 (frontend)
   - IAM Role: Attach role with Bedrock permissions

2. **Install Dependencies**

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@<instance-ip>

# Install Python 3.9+
sudo yum install python3.9 -y

# Install Node.js
curl -sL https://rpm.nodesource.com/setup_16.x | sudo bash -
sudo yum install nodejs -y

# Install Git
sudo yum install git -y
```

3. **Deploy Application**

```bash
# Clone repository
git clone <your-repo-url>
cd <project-directory>

# Setup Python environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r chatbot/requirements.txt

# Install Node dependencies
npm install
cd client && npm install && cd ..

# Initialize database
npm run init-db

# Start services with PM2
npm install -g pm2
pm2 start npm --name "backend" -- run server
pm2 start python --name "chatbot" -- -m chatbot
pm2 start npm --name "frontend" -- run client
pm2 save
pm2 startup
```

### Option 3: AWS Lambda (Advanced)

For serverless deployment, the chatbot service needs modifications:

1. Use API Gateway for HTTP endpoints
2. Store sessions in DynamoDB instead of filesystem
3. Handle cold starts appropriately
4. Configure Lambda timeout (recommended: 30 seconds)

## Monitoring and Logging

### CloudWatch Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /aws/chatbot/shopping-assistant

# View logs
aws logs tail /aws/chatbot/shopping-assistant --follow
```

### Metrics to Monitor

- Request count and latency
- Error rates
- Bedrock API usage and costs
- Active session count
- Memory and CPU usage

### Setting Up Alarms

```bash
# Create alarm for high error rate
aws cloudwatch put-metric-alarm \
  --alarm-name chatbot-high-error-rate \
  --alarm-description "Alert when error rate exceeds 5%" \
  --metric-name ErrorRate \
  --namespace ChatbotService \
  --statistic Average \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold
```

## Security Best Practices

### 1. Credential Management

- **Never commit credentials to version control**
- Use AWS Secrets Manager or Parameter Store for production
- Rotate credentials regularly
- Use IAM roles instead of access keys when possible

### 2. Network Security

- Use HTTPS in production
- Configure security groups to restrict access
- Use VPC for internal communication
- Enable AWS WAF for API protection

### 3. Application Security

- Implement rate limiting
- Add authentication/authorization
- Validate all inputs
- Keep dependencies updated

## Scaling Considerations

### Horizontal Scaling

- Use Application Load Balancer
- Deploy multiple instances
- Implement session affinity or shared session storage

### Session Storage

For production, replace FileSessionManager with:
- **Redis**: For fast, distributed session storage
- **DynamoDB**: For serverless, scalable storage
- **S3**: For cost-effective long-term storage

## Troubleshooting

### Common Issues

#### 1. "Missing AWS credentials"

**Solution**: Verify environment variables are set correctly

```bash
# Check if variables are set
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

# Verify .env file exists and is loaded
cat .env
```

#### 2. "You don't have access to the model"

**Solution**: Request access to Nova Pro in Bedrock console

1. Go to AWS Bedrock Console
2. Navigate to "Model access"
3. Request access to "Nova Pro"
4. Wait for approval

#### 3. "Backend API unreachable"

**Solution**: Verify backend is running and URL is correct

```bash
# Test backend API
curl http://localhost:5000/api/products

# Check BACKEND_API_URL in .env
grep BACKEND_API_URL .env
```

#### 4. "Session storage errors"

**Solution**: Ensure directory exists and has write permissions

```bash
# Create sessions directory
mkdir -p ./sessions

# Set permissions
chmod 755 ./sessions
```

#### 5. "Port already in use"

**Solution**: Change port or kill existing process

```bash
# Find process using port 5001
lsof -i :5001

# Kill process
kill -9 <PID>

# Or change port in .env
echo "CHATBOT_PORT=5002" >> .env
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG

# Run chatbot service
python -m chatbot
```

### Health Checks

```bash
# Check chatbot service health
curl http://localhost:5001/health

# Expected response:
# {"status":"healthy","service":"shopping-assistant-chatbot","active_sessions":0}
```

## Performance Optimization

### 1. Caching

Implement caching for frequently accessed data:
- Product catalog (30-60 seconds)
- Session data (in-memory or Redis)

### 2. Connection Pooling

Use connection pooling for backend API calls:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.3)
adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
session.mount('http://', adapter)
```

### 3. Async Processing

For high-load scenarios, consider async processing:
- Use FastAPI instead of Flask
- Implement async tools
- Use async Bedrock calls

## Cost Optimization

### Bedrock Costs

- Monitor token usage in CloudWatch
- Implement request caching
- Use appropriate temperature settings
- Consider using smaller models for simple queries

### Infrastructure Costs

- Use Fargate Spot for non-critical workloads
- Implement auto-scaling based on demand
- Use S3 for session storage instead of EBS
- Enable CloudWatch Logs retention policies

## Backup and Recovery

### Session Data Backup

```bash
# Backup sessions directory
tar -czf sessions-backup-$(date +%Y%m%d).tar.gz sessions/

# Upload to S3
aws s3 cp sessions-backup-*.tar.gz s3://my-backup-bucket/chatbot-sessions/
```

### Database Backup

```bash
# Backup SQLite database
cp ecommerce.db ecommerce-backup-$(date +%Y%m%d).db

# Upload to S3
aws s3 cp ecommerce-backup-*.db s3://my-backup-bucket/database/
```

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**:
   - Review error logs
   - Check Bedrock usage and costs
   - Monitor response times

2. **Monthly**:
   - Update dependencies
   - Rotate credentials
   - Review and optimize system prompts
   - Clean up old sessions

3. **Quarterly**:
   - Security audit
   - Performance review
   - Cost optimization review

### Getting Help

- Check logs: `tail -f chatbot.log`
- Review CloudWatch metrics
- Test with curl commands
- Enable DEBUG logging

## Additional Resources

- [Strands Agents Documentation](https://strandsagents.com)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
