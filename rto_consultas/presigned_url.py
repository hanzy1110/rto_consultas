import os
import boto3
from dotenv import dotenv_values

from .logging import configure_logger

LOG_FILE = os.environ["LOG_FILE"]
logger = configure_logger(LOG_FILE)


def get_s3_client(bucket_name=None):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not bucket_name:
        bucket_name = os.environ.get("AWS_BUCKET_NAME")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
    )
    return session.client("s3")


def upload_fileobj_to_bucket(file_, s3_key, s3_client, bucket_name):
    if not bucket_name:
        bucket_name = os.environ.get("AWS_BUCKET_NAME")

    s3_client.upload_fileobj(file_, bucket_name, s3_key)
    logger.info(f"FILE {s3_key} UPLOADED TO s3")


# Upload a local file to the S3 bucket
def upload_file_to_bucket(file_path, s3_key, s3_client, bucket_name):
    if not bucket_name:
        bucket_name = os.environ.get("AWS_BUCKET_NAME")

    s3_client.upload_file(file_path, bucket_name, s3_key)
    logger.info(f"FILE {file_path} UPLOADED TO s3")


def generate_presigned_url(object_key, bucket_name=None, expiration=3600):
    """
    Generate a presigned URL for a specific resource in an S3 bucket.

    Args:
        object_key (str): The key (path) of the object/resource within the bucket.
        expiration (int): Expiration time in seconds for the presigned URL (default: 3600 seconds).

    Returns:
        str: The generated presigned URL.
    """
    # env_config = dotenv_values('.env')
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not bucket_name:
        bucket_name = os.environ.get("AWS_BUCKET_NAME")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
    )
    s3_client = session.client("s3")

    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {str(e)}")
        return None


if __name__ == "__main__":
    bucket_name = "your_bucket_name"
    object_key = "path/to/your/resource.ext"

    presigned_url = generate_presigned_url(object_key)
    if presigned_url:
        print(f"Presigned URL: {presigned_url}")
