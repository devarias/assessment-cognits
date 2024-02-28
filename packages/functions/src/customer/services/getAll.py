import json
from typing import Dict
from ..adapters.database import db_engine


def handler(event: Dict, context) -> Dict:
    """
    Handler for retrieving customers with optional filtering based on query string parameters.
    Parses query string parameters from the event and passes them as filters to the repository.
    """
    filters = event.get("queryStringParameters", {})

    filters = {k: v[0] if isinstance(v, list) else v for k, v in filters.items()}

    customers = db_engine.get_filtered(filters=filters)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"customers": customers}),
    }
