from pathlib import PosixPath
from typing import List
import streamlit as st
from datetime import datetime
from dotenv import dotenv_values
from actions import validate_models
from actions.s3_client import S3Tasks
from actions.data_transformations import TableProcessor
from typing import List

config = dotenv_values()
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")


def upload_s3_view(path: List[PosixPath]) -> List[PosixPath]:
    success_tables = []
    with st.expander(label="📁 S3 Upload (Bronze)", expanded=True):
        with st.spinner("Uploading..."):
            for file in path:
                status_ok = S3Tasks().upload_s3(
                    file_name=file,
                    bucket=config["BUCKET"],
                    key=f"{year}/{month}/{day}/{file.name}",
                )
                if status_ok:
                    st.success(f"{file.stem} ✅")
                    success_tables.append(file)
                else:
                    st.error(f"🚨 Error uploading {file.stem}. Please review the logs.")
    return success_tables


def pydantic_view(files: List[PosixPath]) -> List[PosixPath]:
    success_tables = []
    with st.expander(label="📝 Data Contracts", expanded=True):
        with st.spinner(text="Validating..."):
            for file in files:
                row_errors = validate_models.validate_model(file)
                if not row_errors:
                    st.success(f"{file.stem} ✅")
                    success_tables.append(file)
                else:
                    st.error(f"🚨 {file.stem} has violation(s). Please review the logs.")
        return success_tables


def transformation_to_postgres_view(files: List[PosixPath]) -> List[PosixPath]:
    success_tables = []
    with st.expander(label="💾 Database Insert", expanded=True):
        with st.spinner(text="Inserting..."):
            for file in files:
                rows = TableProcessor(path=file).run_pipeline()
                if rows:
                    st.success(f"{file.stem} ✅")
                    success_tables.append(file)
                else:
                    st.error(
                        f"🚨 Error inserting {file.stem} to database. Please review the logs."
                    )
        return success_tables
