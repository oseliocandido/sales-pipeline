import streamlit as st
from datetime import datetime, timedelta
from dotenv import dotenv_values
from pathlib import Path
from tasks.s3.client import download_s3, upload_s3
import time
from subpro import call_dbt
from streamlit_functions import pydantic_validation
from typing import List
import pandas as pd


def main() -> None:
    st.set_page_config(
        page_title="Data",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            # FIXME: DOING nothing
            "Get Help": "https://www.extremelycoolapp.com/help",
            "Report a bug": "https://www.extremelycoolapp.com/bug",
            "About": "# This is a header. This is an *extremely* cool app!",
        },
    )

    # TODO: Put description nice here maybe witf faker
    st.sidebar.markdown("# Pipeline")
    st.sidebar.write(
        "Generate fake data with local csvs in append/overwrite mode and valid/invalid data contract"
    )
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        overwrite_flag = st.radio(
            label="Generation Mode", options=["Overwrite", "Append"], key=300
        )
    with col2:
        valid_data_flag = st.radio(
            label="Data Contract Type", options=["Valid", "Invalid"], key=500
        )
    status = st.sidebar.button("Generate Data", use_container_width=True)

    # FIXME: Change this to another place
    config = dotenv_values()

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    base_data_path = Path.cwd() / "data"
    read_files_path = base_data_path.glob(f"{valid_data_flag.lower()}/*.csv")


if __name__ == "__main__":
    main()
