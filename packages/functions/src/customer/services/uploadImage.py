import base64
import json
from typing import Dict
from ..adapters.database import db_engine


def handler(event: Dict, context) -> Dict:
    """
    AWS Lambda handler for uploading an image for a customer.

    :param event: Dictionary with input data, including the base64-encoded image and the customer ID.
    :param context: AWS Lambda context object, not used in this function.
    :return: A dictionary with the operation result.
    """
    customer_id = event["pathParameters"]["id"]
    image_data = event["body"]
    content_type = event["headers"].get("Content-Type", "image/jpeg")

    image_bytes = base64.b64decode(image_data)

    result_message = db_engine.upload_image(
        customer_id, image_bytes, content_type)

    if not result_message:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Customer not found"})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": result_message})
    }
