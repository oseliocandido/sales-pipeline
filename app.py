import streamlit as st
from datetime import datetime
from dotenv import dotenv_values
from pathlib import Path
from tasks.s3.client import download_s3, upload_s3
import pandas as pd


date_now = datetime.now()
year = date_now.strftime("%Y")
month = date_now.strftime("%m")
day = date_now.strftime("%d")


config = dotenv_values()
st.set_page_config(page_title="Inicio do app", page_icon="🌐")

path = Path.cwd() / "data" / "Product.csv"

if st.button(label="Upload s3"):
    with st.spinner("Uploading to s3..."):
        status = upload_s3(
            file_name=path,
            bucket=config["BUCKET"],
            key=f"{year}/{month}/{day}/{path.name}",
        )
        if status:
            st.success("Arquivo upado com sucesso")
        else:
            st.error("Deu ruim")

# Download from S3 and render in memory
if st.button("Download from S3"):
    with st.spinner("Downloading from S3..."):
        file_downloaded = download_s3(config["BUCKET"], "2024/05/17/Product.csv")

    if file_downloaded:
        st.success("Download successful!")
        with st.spinner("Rendering...."):
            s3_data = file_downloaded
            s3_data.seek(0)
            df = pd.read_csv(s3_data, engine="pyarrow", delimiter="\t")
            st.dataframe(df)
    else:
        st.error("Download failed. Check logs for details.")
