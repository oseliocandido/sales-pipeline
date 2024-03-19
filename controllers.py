import streamlit as st
from pathlib import PosixPath
from time import sleep
from validations import validate
from typing import List


def pydantic_validation(path: PosixPath) -> List:
    file_error = []
    with st.spinner(text="Validating..."):
        for file in path:
            sleep(2.0)
            validation_errors = validate.validate_model(file)
            if not validation_errors:
                st.success(f"{file.stem} ✅")
            else:
                file_error.append(1)
                st.error(f"🚨 {file.stem} has violation(s). Please review the logs.")
                continue
    return file_error
