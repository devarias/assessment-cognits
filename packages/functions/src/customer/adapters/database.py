import os
from ..repositories.customer import CustomerRepository

DYNAMODB_TABLE_NAME = os.environ["DYNAMODB_TABLE_NAME"]
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

db_engine = CustomerRepository(
    dynamodb_table_name=DYNAMODB_TABLE_NAME, s3_bucket_name=S3_BUCKET_NAME)
