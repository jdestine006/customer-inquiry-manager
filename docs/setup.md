# Setup Guide — AI Customer Inquiry Manager

This guide walks through how to recreate the AI Customer Inquiry Manager from scratch using AWS services and a React frontend.

⸻

## Architecture Overview

    User
     ↓
    Amplify Hosting
     ↓
    API Gateway
     ↓
    Lambda
     ↓
    Amazon Bedrock
     ↓
    DynamoDB


⸻

## Prerequisites
	•	AWS account
	•	Node.js installed
	•	npm installed
	•	Git installed
	•	AWS CLI (optional)

⸻

1. Create DynamoDB Table

Go to:

    AWS Console → DynamoDB → Create Table

Settings:

  Field	                      Value
Table name	          CustomerInquiries
Partition key	           inquiryId
Capacity mode	           On-demand

After creating the table, note the table name for Lambda configuration.

⸻

2. Create Lambda Function

Go to:

    AWS Console → Lambda → Create function

Settings:
```
Field	                    Value
Function name	          inquiry-handler
Runtime	                    Python
Permissions	          Create new execution role
```

Add the following IAM permissions to the role:

    AmazonDynamoDBFullAccess
    AmazonBedrockFullAccess
    CloudWatchLogsFullAccess


⸻

3. Add Lambda Code

Example structure:

    backend/inquiry_handler.py

The Lambda function should:
	1.	Receive inquiry data
	2.	Send prompt to Amazon Bedrock
	3.	Generate AI response
	4.	Store inquiry in DynamoDB
	5.	Return response to client

Expected response format:

    {
      "inquiryId": "...",
      "aiResponse": "Generated response"
    }


⸻

4. Configure Amazon Bedrock

Go to:

    AWS Console → Bedrock → Model catalog

Enable a model such as:

    Amazon Nova

Update the Lambda function to invoke the model.

⸻

5. Create API Gateway

Go to:

    AWS Console → API Gateway → Create API

Choose:

HTTP API

Configuration:
```
Setting:               Value: 
Route	              POST /inquiries
Integration	       Lambda → inquiry-handler
Stage	                  dev
```
Example endpoint:

    https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/inquiries


⸻

6. Configure CORS

In API Gateway:

    Allow origins: *
    Allow methods: POST, OPTIONS
    Allow headers: content-type

Deploy the API.

⸻

7. Create the React Frontend

Create a React app using Vite:

    npm create vite@latest customer-inquiry-frontend
    cd customer-inquiry-frontend
    npm install


⸻

8. Connect Frontend to API

Update App.jsx:

    const API_BASE = "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/dev";

Submit requests to:

    ${API_BASE}/inquiries


⸻

9. Run Locally

Start the development server:

    npm run dev

Visit:

    http://localhost:5173

Submit a test inquiry to verify the system.

⸻

10. Build the Frontend

Generate the production build:

    npm run build

This creates a:

    dist/

folder containing the static site.

⸻

11. Deploy with AWS Amplify

Go to:

    AWS Console → Amplify → New App

Choose:

Deploy without Git

Upload the contents of the dist folder.

Amplify will generate a URL such as:

    https://your-app.amplifyapp.com


⸻

12. Update API CORS

Allow the Amplify domain:

    https://your-app.amplifyapp.com

Redeploy the API if needed.

⸻

Final Result

Users can now:
	1.	Submit inquiries from the web interface
	2.	Receive AI-generated responses
	3.	Store inquiries in DynamoDB
	4.	View responses instantly

⸻
