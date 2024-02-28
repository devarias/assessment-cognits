import json
from datetime import datetime
from typing import Dict
from ..adapters.database import db_engine


def handler(event: Dict, context) -> Dict:
    """
    AWS Lambda handler for creating a new customer.

    :param event: The Lambda event.
    :param context: The Lambda execution context.
    :return: A dictionary with the operation result.
    """
    try:
        customer_data = json.loads(event["body"])

        customer_data["creationDate"] = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

        result_message = db_engine.create(customer_data)

        return {"statusCode": 201, "body": json.dumps({"message": result_message})}
    except Exception:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to create customer"}),
        }
