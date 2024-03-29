from io import BytesIO
from dotenv import dotenv_values
from botocore.exceptions import ClientError
from pathlib import PosixPath
from boto3 import client
from utils.logger import logger

config = dotenv_values()


class S3Tasks:
    def __init__(self):
        self.config = dotenv_values()
        self.s3_client = client(
            "s3",
            aws_access_key_id=self.config["AWS_ACCESS_KEY"],
            aws_secret_access_key=self.config["AWS_SECRET_ACCESS_KEY"],
        )

    def upload_s3(self, file_name: PosixPath, bucket: str, key: str) -> bool:
        try:
            self.s3_client.upload_file(Filename=file_name, Bucket=bucket, Key=key)
        except ClientError as error:
            logger.error(error)
            return False
        return True
