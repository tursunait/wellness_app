import boto3
import json
import base64
from typing import Optional
from features.env_loader import load_env_variables

# Load .env file variables
load_env_variables()

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")


def call_claude(prompt: str, image: Optional[bytes] = None):
    """
    Call Claude 3 Sonnet with optional image (bytes).
    """
    messages = []

    if image:
        # Convert image bytes to base64
        encoded_image = base64.b64encode(image).decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": encoded_image,
                        },
                    },
                ],
            }
        ]
    else:
        # Text-only prompt
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 400,
        "top_k": 250,
        "temperature": 1,
        "top_p": 0.999,
        "stop_sequences": [],
        "messages": messages,
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
