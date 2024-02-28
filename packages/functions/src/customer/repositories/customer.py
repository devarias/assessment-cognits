from typing import Dict, Optional, List
import boto3
from botocore.exceptions import ClientError
from botocore.client import BaseClient
import uuid


class CustomerRepository:
    """Handles CRUD operations on DynamoDB and image uploads to S3 for customers."""

    def __init__(self, dynamodb_table_name: str, s3_bucket_name: Optional[str] = None):
        """
        Initializes the repository with the specified DynamoDB table and an optional S3 bucket.

        :param dynamodb_table_name: Name of the DynamoDB table for customer data.
        :param s3_bucket_name: Optional; Name of the S3 bucket for customer images. Default is None.
        """
        self.dynamodb_table_name: str = dynamodb_table_name
        self.s3_bucket_name: Optional[str] = s3_bucket_name
        self.dynamodb: BaseClient = boto3.resource("dynamodb")
        self.s3: BaseClient = boto3.client("s3")
        self.table = self.dynamodb.Table(dynamodb_table_name)

    def create(self, customer_data: Dict) -> Dict:
        """
        Creates a new customer in the DynamoDB table.

        :param customer_data: A dictionary containing customer data.
        :return: Success message or error message.
        """
        try:
            self.table.put_item(
                Item=customer_data, Expected={"customerId": {"Exists": False}}
            )
            return customer_data
        except ClientError:
            return "Error creating customer"

    def get_by_id(self, customer_id: str) -> Dict:
        """
        Retrieves customer details by ID.

        :param customer_id: The customer"s ID.
        :return: Customer data as a dictionary or an error message.
        """
        try:
            response = self.table.get_item(Key={"customerId": customer_id})
            return response.get("Item", {})
        except ClientError:
            return "Error retrieving customer"

    def update(self, customer_id: str, update_data: Dict) -> Dict:
        """
        Updates an existing customer"s details.

        :param customer_id: The customer"s ID to update.
        :param update_data: A dictionary containing data to update.
        :return: Update action response or error message.
        """
        try:
            user_exists = self.get_by_id(customer_id)
            if not user_exists:
                return user_exists
            response = self.table.update_item(
                Key={"customerId": customer_id},
                UpdateExpression="set "
                + ", ".join(["{}=:{}".format(k, k) for k in update_data.keys()]),
                ExpressionAttributeValues={
                    ":{}".format(k): v for k, v in update_data.items()
                },
                ReturnValues="UPDATED_NEW",
            )
            return response.get("Attributes", {})
        except ClientError as e:
            return "Error updating customer"

    def delete(self, customer_id: str) -> str:
        """
        Deletes a customer from the DynamoDB table.

        :param customer_id: The ID of the customer to delete.
        :return: Success message or error message.
        """
        try:
            user_exists = self.get_by_id(customer_id)
            if not user_exists:
                return user_exists
            self.table.delete_item(Key={"customerId": customer_id})
            return "Customer deleted successfully."
        except ClientError as e:
            return "Error deleting customer"

    def upload_image(
        self, customer_id: str, image_data: bytes, content_type: str
    ) -> str:
        """Uploads a customer"s image to S3 and updates customer data with the image URL."""
        try:
            file_name = "{}/{}".format(customer_id, uuid.uuid4().hex)

            self.s3.put_object(
                Bucket=self.s3_bucket_name,
                Key=file_name,
                Body=image_data,
                ContentType=content_type,
            )

            image_url = "https://{}.s3.amazonaws.com/{}".format(
                self.s3_bucket_name, file_name
            )

            self.table.update_item(
                Key={"customerId": customer_id},
                UpdateExpression="SET imageUrl = :val",
                ExpressionAttributeValues={":val": image_url},
                ReturnValues="UPDATED_NEW",
            )

            return "Image uploaded successfully. URL: {}".format(image_url)
        except ClientError:
            return "Failed to upload image."

    def get_filtered(self, filters=None) -> List[Dict]:
        """
        Retrieves customers based on the specified filters.

        Parameters:
        - filters (dict): A dictionary where keys are attribute names (e.g., "firstName", "postalCode")
                          and values are the corresponding values to filter by.

        Returns:
        - list: A list of dictionaries, each representing a customer matching the filters.
        """
        try:
            filter_expressions = []
            expression_attribute_values = {}
            for i, (key, value) in enumerate(filters.items(), start=1):
                if key in ["postalCode", "firstName", "lastName", "city", "country"]:
                    filter_expressions.append("begins_with({}, :val{})".format(key, i))
                expression_attribute_values[":val{}".format(i)] = value

            combined_filter_expression = " AND ".join(filter_expressions)

            if not len(expression_attribute_values):
                return self.table.scan().get("Items", [])
            else:
                response = self.table.scan(
                    FilterExpression=combined_filter_expression,
                    ExpressionAttributeValues=expression_attribute_values,
                )

            return response.get("Items", [])
        except ClientError as e:
            print("Error scanning customers")
            print(e)
            return []
