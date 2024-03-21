from io import BytesIO
from dotenv import dotenv_values
from botocore.exceptions import ClientError
from pathlib import PosixPath
from boto3 import client

config = dotenv_values()


class S3Tasks:
    def __init__(self):
        self.config = dotenv_values()
        self.s3_client = client(
            "s3",
            aws_access_key_id=self.config["AWS_ACCESS_KEY"],
            aws_secret_access_key=self.config["AWS_SECRET_ACCESS_KEY"],
        )

    # Botar dps pra updr parquet e ler com duckdb
    def upload_s3(self, file_name: PosixPath, bucket: str, key: str) -> bool:
        try:
            self.s3_client.upload_file(Filename=file_name, Bucket=bucket, Key=key)
        except ClientError:
            return False
        return True

    def download_s3(self, bucket: str, key: str) -> BytesIO:
        s3_io_data = BytesIO()
        try:
            self.s3_client.download_fileobj(bucket, key, s3_io_data)
        except ClientError as e:
            return False
        return s3_io_data
