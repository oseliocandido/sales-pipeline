from pathlib import PosixPath
from typing import List
import streamlit as st
from time import sleep
from datetime import datetime
from dotenv import dotenv_values
from validations import validate
from tasks.s3 import client
import boto3
from botocore.exceptions import ClientError
from io import BytesIO
import pandas as pd

config = dotenv_values()
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")


def pydantic_view(path: List[PosixPath]) -> List:
    with st.expander(label="Data Contracts", expanded=True):
        errors = []
        with st.spinner(text="Validating..."):
            for file in path:
                sleep(2)
                validation_errors = validate.validate_model(file)
                if not validation_errors:
                    st.success(f"{file.stem} ✅")
                else:
                    errors.append(1)
                    st.error(f"🚨 {file.stem} has violation(s). Please review the logs.")
                    continue
        return errors


def upload_s3_view(path: List[PosixPath]) -> List:
    with st.expander(label="📁 S3 Upload", expanded=True):
        errors = []
        with st.spinner("Uploading..."):
            for file in path:
                sleep(2)
                status = client.upload_s3(
                    file_name=file,
                    bucket=config["BUCKET"],
                    key=f"{year}/{month}/{day}/{file.name}",
                )
                if status:
                    st.success(f"{file.stem} ✅")
                else:
                    errors.append(1)
                    st.error(f"🚨 Error uploading {file.stem}. Please review the logs.")
    return errors


def download_s3_view(aws_files: List[PosixPath]) -> List:
    mapping_bytes = {}
    with st.expander(label="S3 Download", expanded=True):
        with st.spinner(text="Downloading..."):
            for file in aws_files:
                sleep(2)
                data = client.download_s3(
                    bucket=config["BUCKET"], key=f"{year}/{month}/{day}/{file.name}"
                )
                if data:
                    data.seek(0)
                    mapping_bytes[file.name] = data
                    st.success(f"{file.stem} ✅")
                    st.dataframe(
                        pd.read_csv(
                            mapping_bytes[file.name], engine="pyarrow", delimiter="\t"
                        )
                    )
                else:
                    st.error(f"🚨 Error dowloading {file.stem}. Please review the logs.")
        return mapping_bytes
