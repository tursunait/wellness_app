import uuid
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("wellness-app")


def convert_floats_to_decimal(obj):
    """Recursively converts float values to Decimal."""
    if isinstance(obj, list):
        return [convert_floats_to_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_floats_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj


def clean_profile_data(profile: dict) -> dict:
    """Cleans profile and converts all floats to Decimal"""
    profile = {k: v for k, v in profile.items() if v is not None and v != ""}
    return convert_floats_to_decimal(profile)


def save_profile_to_dynamodb(profile: dict) -> str:
    user_id = str(uuid.uuid4())
    profile["user_id"] = user_id

    clean_profile = clean_profile_data(profile)
    table.put_item(Item=clean_profile)

    return user_id
