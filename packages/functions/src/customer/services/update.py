import json
from typing import Dict
from datetime import datetime
from ..adapters.database import db_engine


def handler(event: Dict, context) -> Dict:
    """
    AWS Lambda handler for updating a customer"s information.

    :param event: Dictionary with input data. Expected to have `customer_id` and `update_data`.
    :param context: AWS Lambda context object (not used in this function).
    :return: A dictionary with the operation result.
    """
    data = json.loads(event["body"])
    customer_id = event["pathParameters"]["id"]
    data["lastUpdate"] = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

    result_message = db_engine.update(customer_id, data)


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
