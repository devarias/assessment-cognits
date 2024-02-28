import os
import jwt
import uuid
import boto3
from typing import Dict


def handler(event: Dict, context) -> Dict:
    jwt_key = get_secret()

    token = event["authorizationToken"]
    print(event)

    try:
        valid = jwt.decode(token, key=jwt_key, algorithms=["HS256"])
        print(valid)
        auth = "Allow"
    except:
        auth = "Deny"

    account_id = os.environ["ACCOUNT_ID"]
    api_id = os.environ["API_ID"]
    stage = os.environ["SST_STAGE"]
    method = event["httpMethod"]
    resource = (
        event["requestContext"]["resourcePath"]
        if not len(event["pathParameters"])
        else replace_placeholders_with_values(
            event["requestContext"]["resourcePath"], event["pathParameters"]
        )
    )
    principal_id = uuid.uuid4()

    authResponse = {
        "principalId": str(principal_id),
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Resource": [
                        "arn:aws:execute-api:us-east-1:{}:{}/{}/{}{}".format(
                            account_id, api_id, stage, method, resource
                        )
                    ],
                    "Effect": auth,
                }
            ],
        },
    }
    print(authResponse)
    return authResponse


def replace_placeholders_with_values(url_template: str, values_dict: dict) -> str:
    """
    Replaces placeholders in the URL template with values from the provided dictionary.

    Parameters:
    - url_template (str): A URL path string containing placeholders, e.g., "customers/{id}/{another_id}".
    - values_dict (dict): A dictionary where keys match the placeholders in the URL template and values are the replacement values.

    Returns:
    - str: The URL path string with placeholders replaced by corresponding values from the dictionary.
    """
    try:
        modified_url = url_template.format(**values_dict)
    except KeyError as e:
        modified_url = url_template

    return modified_url


def get_secret():
    ssm = boto3.client("ssm", region_name=os.environ["AWS_REGION"])
    try:
        parameter = ssm.get_parameter(
            Name="{}Secret/JWT_KEY/value".format(os.environ["SST_SSM_PREFIX"]),
            WithDecryption=True,
        )
        return parameter["Parameter"]["Value"]
    except:
        raise EnvironmentError("Missing environment variable")
