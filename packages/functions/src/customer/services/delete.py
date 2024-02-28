import json
from typing import Dict
from ..adapters.database import db_engine


def handler(event: Dict, context) -> Dict:
    """
    AWS Lambda handler for deleting a customer"s information.

    :param event: Dictionary with input data. Expected to have `customer_id`.
    :param context: AWS Lambda context object (not used in this function).
    :return: A dictionary with the operation result.
    """
    customer_id = event["pathParameters"]["id"]

    result_message = db_engine.delete(customer_id)

    if not result_message:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Customer not found"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": result_message}),
    }
