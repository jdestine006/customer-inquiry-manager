import json
import os
import time
import uuid
from datetime import datetime, timezone
import boto3

dynamodb = boto3.resource("dynamodb")
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

TABLE_NAME = os.environ["TABLE_NAME"]
MODEL_ID = os.environ["MODEL_ID"]

table = dynamodb.Table(TABLE_NAME)

def _resp(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            # Dev-friendly CORS. We'll tighten this once CloudFront is set up.
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
        "body": json.dumps(body),
    }

def _get_body(event: dict) -> dict:
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        # Not expected for JSON posts, but handle safely.
        import base64
        raw = base64.b64decode(raw).decode("utf-8")
    return json.loads(raw)

def _invoke_bedrock(prompt: str):

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 300,
            "temperature": 0.3
        }
    }

    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    return result["output"]["message"]["content"][0]["text"]

def lambda_handler(event, context):
    # Handle preflight CORS
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return _resp(200, {"ok": True})

    try:
        body = _get_body(event)
        name = (body.get("name") or "").strip()
        email = (body.get("email") or "").strip()
        message = (body.get("message") or "").strip()

        if not message:
            return _resp(400, {"error": "message is required"})

        inquiry_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        prompt = f"""
            You are Jarvis, a friendly and helpful customer support specialist. 
            Write a helpful and professional response to this customer inquiry.
            Customer name: {name}
            Customer email: {email}
            Inquiry: {message}

            Sign the response with:

            Best Regards,
            Jarvis 
            AI Customer Support Specialist
            """

        t0 = time.time()
        ai_response = _invoke_bedrock(prompt)
        latency_ms = int((time.time() - t0) * 1000)

        item = {
            "inquiryId": inquiry_id,
            "createdAt": created_at,
            "name": name,
            "email": email,
            "message": message,
            "status": "RESPONDED",
            "aiResponse": ai_response,
            "modelId": MODEL_ID,
            "latencyMs": latency_ms,
        }

        table.put_item(Item=item)

        return _resp(200, {"inquiryId": inquiry_id, "aiResponse": ai_response})

    except Exception as e:
        # CloudWatch logs will show full stack trace
        print("ERROR:", repr(e))
        return _resp(500, {"error": "internal_error", "details": str(e)[:500]})
