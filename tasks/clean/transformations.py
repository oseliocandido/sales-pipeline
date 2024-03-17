# TODO:

## Products Table
## Standard cost column name must be replace em empyt space bettworns with  char _
## Trim in specific column os specifc table jmaybe this one

## In Sales Table, it will make parse transformatio in the Target Month column after is ok in pydantic

import pandas as pd
from dotenv import dotenv_values
import boto3
from botocore.exceptions import ClientError
from io import BytesIO

config = dotenv_values()


# Working nicely!
def download_s3_file() -> None:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=config["AWS_ACCESS_KEY"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
    )

    local_file_path = "s3_file.csv"
    try:
        with open(local_file_path, "wb") as data:
            s3_client.download_fileobj(config["BUCKET"], "2024/03/17/Product.csv", data)
    except ClientError as e:
        print(f"Error: {str(e)}")
        return False
    return True


def s3_io() -> BytesIO:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=config["AWS_ACCESS_KEY"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
    )
    try:
        s3_io_data = BytesIO()
        s3_client.download_fileobj(
            config["BUCKET"], "2024/03/17/Product.csv", s3_io_data
        )
    except ClientError as e:
        print(f"Error: {str(e)}")
        return False
    return s3_io_data


if __name__ == "__main__":
    s3_data = s3_io()
    s3_data.seek(0)
    df = pd.read_csv(s3_data, engine="pyarrow", delimiter="\t")
    print(df.head())
