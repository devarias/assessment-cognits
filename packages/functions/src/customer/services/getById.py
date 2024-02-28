import json
from typing import Dict
from ..adapters.database import db_engine


def handler(event: Dict, context) -> Dict:
    """
    AWS Lambda handler for retrieving a customer"s information by ID.

    :param event: Dictionary with input data, expected to have `id`.
    :param context: AWS Lambda context object, not used in this function.
    :return: A dictionary with the customer data or an error message.
    """
    customer_id = event["pathParameters"]["id"]

    customer_data = db_engine.get_by_id(customer_id)

    if not customer_data:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Customer not found"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(customer_data),
    }
