from pathlib import PosixPath
from typing import List
import streamlit as st
from datetime import datetime
from dotenv import dotenv_values
from actions import validate_models
from actions.s3_client import S3Tasks
from actions.data_transformations import TableProcessor


config = dotenv_values()
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")


def pydantic_view(files: List[PosixPath]) -> bool:
    with st.expander(label="Data Contracts", expanded=True):
        error_table = False
        with st.spinner(text="Validating..."):
            for file in files:
                row_errors = validate_models.validate_model(file)
                if not row_errors:
                    st.success(f"{file.stem} ✅")
                else:
                    error_table = True
                    st.error(f"🚨 {file.stem} has violation(s). Please review the logs.")
        return error_table


def upload_s3_view(path: List[PosixPath]) -> bool:
    with st.expander(label="📁 S3 Upload", expanded=True):
        error_table = False
        with st.spinner("Uploading..."):
            for file in path:
                status_ok = S3Tasks().upload_s3(
                    file_name=file,
                    bucket=config["BUCKET"],
                    key=f"{year}/{month}/{day}/{file.name}",
                )
                if status_ok:
                    st.success(f"{file.stem} ✅")
                else:
                    error_table = True
                    st.error(f"🚨 Error uploading {file.stem}. Please review the logs.")
    return error_table


def transformation_to_postgres_view(files: List[PosixPath]) -> list[bool]:
    error_table = False
    with st.expander(label="Database Insert", expanded=True):
        with st.spinner(text="Inserting..."):
            for file in files:
                rows = TableProcessor(path=file).run_pipeline()
                if rows:
                    st.success(f"{file.stem} Inserted ✅")
                else:
                    error_table = True
                    st.error(
                        f"🚨 Error inserting {file.stem} to database. Please review the logs."
                    )
        return error_table


# Donwload AWS
# def download_s3_view(aws_files: List[PosixPath]) -> dict[str,BytesIO]:
#     mapping_bytes = {}
#     with st.expander(label="S3 Download", expanded=True):
#         with st.spinner(text="Downloading..."):
#             for file in aws_files:
#                 sleep(1.5)
#                 data = S3Tasks().download_s3(bucket=config["BUCKET_BRONZE"], key=f"{year}/{month}/{19}/{file.name}")
#                 if data:
#                     data.seek(0)
#                     mapping_bytes[file.stem] = data
#                     st.success(f"{file.stem} ✅")
#                     st.info(f'{file.stem} Preview...')
#                     st.dataframe(pd.read_csv(mapping_bytes[file.stem], engine="pyarrow", delimiter="\t").head(3))
#                 else:
#                     st.error(f"🚨 Error dowloading {file.stem}. Please review the logs.")
#         return mapping_bytes
