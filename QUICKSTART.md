# Quick Start Guide - Shopping Assistant Chatbot

Get your Shopping Assistant Chatbot up and running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- Node.js 16+ installed
- AWS Account with Bedrock access
- Access to Bedrock Nova Pro model

## Step 1: AWS Setup (5 minutes)

### Request Bedrock Model Access

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Click "Model access" in the left sidebar
3. Click "Manage model access"
4. Find and select "Nova Pro"
5. Click "Request model access"
6. Accept terms and wait for approval (usually instant)

### Get AWS Credentials

**Option A: Create IAM User (Development)**

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click "Users" → "Add users"
3. Name: `chatbot-dev`
4. Select "Programmatic access"
5. Attach policy with these permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Action": [
         "bedrock:InvokeModel",
         "bedrock:InvokeModelWithResponseStream"
       ],
       "Resource": "*"
     }]
   }
   ```
6. Save your Access Key ID and Secret Access Key

**Option B: Use Existing Credentials**

If you already have AWS CLI configured:
```bash
cat ~/.aws/credentials
```

## Step 2: Configure Environment (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

Add your AWS credentials:
```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-west-2
```

## Step 3: Install Dependencies (2 minutes)

### Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r chatbot/requirements.txt
```

### Node.js Dependencies (if not already installed)

```bash
# Install root dependencies
npm install

# Install client dependencies
cd client && npm install && cd ..
```

## Step 4: Initialize Database (30 seconds)

```bash
npm run init-db
```

## Step 5: Start Services (1 minute)

Open three terminal windows:

### Terminal 1: Backend API
```bash
npm run server
```
Wait for: `Server running on port 5000`

### Terminal 2: Chatbot Service
```bash
source venv/bin/activate  # If not already activated
python -m chatbot
```
Wait for: `Starting chatbot service on port 5001`

### Terminal 3: Frontend
```bash
npm run client
```
Wait for: `Compiled successfully!`

## Step 6: Test It Out! (30 seconds)

1. Open browser to http://localhost:3000
2. Click the chat button (💬) in the bottom right
3. Try these commands:
   - "Show me all products"
   - "Tell me about product 1"
   - "Add product 1 to my cart"
   - "What's in my cart?"
   - "Recommend some products"

## Verification Checklist

✓ Backend API running on port 5000
✓ Chatbot service running on port 5001
✓ Frontend running on port 3000
✓ Chat button visible on homepage
✓ Chatbot responds to messages

## Quick Test Commands

### Test Backend API
```bash
curl http://localhost:5000/api/products
```

### Test Chatbot Service
```bash
curl http://localhost:5001/health
```

### Test Chat Endpoint
```bash
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","session_id":"test-123"}'
```

## Troubleshooting

### "Missing AWS credentials"
- Check .env file exists
- Verify credentials are correct
- Ensure .env is in project root

### "You don't have access to the model"
- Complete Step 1: Request Bedrock model access
- Wait a few minutes and try again
- Check correct AWS region (us-west-2)

### "Backend API unreachable"
- Ensure Terminal 1 shows backend running
- Check port 5000 is not in use
- Try: `curl http://localhost:5000/api/products`

### "Port already in use"
- Kill existing process: `lsof -i :5001` then `kill -9 <PID>`
- Or change port in .env: `CHATBOT_PORT=5002`

### "Module not found"
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r chatbot/requirements.txt`

## What's Next?

### Explore Features
- Browse products conversationally
- Add items to cart
- Get product recommendations
- View product reviews
- Manage cart quantities

### Read Documentation
- `chatbot/README.md` - Detailed service documentation
- `DEPLOYMENT.md` - Production deployment guide
- `IMPLEMENTATION_SUMMARY.md` - Complete implementation details

### Deploy to Production
See `DEPLOYMENT.md` for:
- Docker deployment
- AWS ECS/Fargate deployment
- EC2 deployment
- Monitoring and scaling

## Example Conversations

### Browse Products
```
You: Show me all products
Bot: Here are the available products:
     📱 Smartphone - $699.99
     💻 Laptop - $1299.99
     ...
```

### Add to Cart
```
You: Add the smartphone to my cart
Bot: Successfully added 1 item(s) to your cart!
```

### Get Recommendations
```
You: Can you recommend something?
Bot: Based on our catalog, I'd recommend...
```

### View Cart
```
You: What's in my cart?
Bot: Your Shopping Cart:
     📱 Smartphone x 1 - $699.99
     Total: $699.99
```

## Support

- Check logs: `tail -f chatbot.log`
- Enable debug: `export LOG_LEVEL=DEBUG`
- Run verification: `python3 verify_setup.py`

## Success!

You now have a fully functional AI-powered shopping assistant! 🎉

The chatbot can:
- ✓ Browse products
- ✓ Manage shopping cart
- ✓ Provide recommendations
- ✓ Answer questions
- ✓ Remember conversation context

Happy shopping! 🛒
