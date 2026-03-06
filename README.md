# AI Customer Inquiry Manager 

## Overview
A full-stack serverless AI-powered support system built using AWS services. Customers can submit inquiries through a web interface, and the system automatically generates a professional response using Amazon Bedrock AI models.  

The application is designed using a modern serverless architecture with a React frontend and AWS-managed backend services.  

The application is hosted using AWS Amplify, and features a serverless API built with API Gateway and Lambda.  

Customer inquires and responses are collected and stored in a DynamoDB table for historical record-keeping.

## Key AWS Services Used
    AWS Amplify
    S3
    AWS Bedrock
    DynamoDB
    API Gateway
    AWS Lambda
    IAM 

### Frontend Technologies
    React 
    Vite
    JavaScript
    AWS Amplify

### Backend Technologies
    AWS Lambda
    API Gateway (HTTP API)
    DynamoDB

## Key Features  
 ### AI-Powered Support System Functionality
 AI-generated customer support responses using Amazon Bedrock
 ### Serverless Architecture
 Serverless API built with API Gateway & Lambda. Inquiries and responses stored on DynamoDB
 ### UI/UX Design
 Responsive React Frontend, hosted using AWS Amplify
 ### End-to-End Cloud Architecture
 Fully managed by AWS. Offers little to no provisioning of resources

 ## How it Works

1. User submits a support inquiry from the web.
2. The frontend sends a request to API Gateway
3. API Gateway triggers a Lambda function.
4. Lambda function sends the inquiry to Amazon Bedrock for AI-generated response
5. The inquiry and response are stored in DynamoDB
6. The response is returned to the frontend and displayed to the user

### Example Response  
     Subject: System Status Update

     Hi Jonathan,

    Thank you for reaching out! I'm pleased to inform you that all our systems are fully operational and running smoothly  
    today. If you encounter any issues or need further assistance, please don't hesitate to let me know.

    Best Regards,  
    Jarvis  
    AI Customer Support Specialist
