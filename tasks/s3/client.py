from io import BytesIO
from dotenv import dotenv_values
from botocore.exceptions import ClientError
import boto3
from pathlib import PosixPath

config = dotenv_values()


# Botar dps pra updr parquet e ler com duckdb
def upload_s3(file_name: PosixPath, bucket: str, key: str) -> bool:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=config["AWS_ACCESS_KEY"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
    )
    try:
        s3_client.upload_file(Filename=file_name, Bucket=bucket, Key=key)
    except ClientError:
        return False
    return True


def download_s3(bucket: str, key: str) -> BytesIO:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=config["AWS_ACCESS_KEY"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
    )
    try:
        s3_io_data = BytesIO()
        s3_client.download_fileobj(bucket, key, s3_io_data)
    except ClientError as e:
        print(f"Error: {str(e)}")
        return False
    return s3_io_data
