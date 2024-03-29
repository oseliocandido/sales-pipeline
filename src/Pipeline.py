import streamlit as st
from pathlib import PosixPath, Path
from views.view_actions import pydantic_view
from views.view_actions import upload_s3_view
from views.view_actions import transformation_to_postgres_view


def upload_to_s3(local_files_path):
    upload_success_tables = upload_s3_view(local_files_path)
    if not upload_success_tables:
        st.sidebar.error("Uploaded failed! Aborting Pipeline.. ❌")
        st.stop()
    else:
        st.sidebar.success("Upload to S3 🎯")
    return upload_success_tables


def validate_data(upload_success_tables):
    pydantic_success_tables = pydantic_view(upload_success_tables)
    if not pydantic_success_tables:
        st.sidebar.error("Validation failed! Aborting Pipeline.. ❌")
        st.stop()
    else:
        st.sidebar.success("Data Contract 🎯")
    return pydantic_success_tables


def insert_to_database(pydantic_success_tables):
    pg_success_tables = transformation_to_postgres_view(pydantic_success_tables)
    if not pg_success_tables:
        st.sidebar.error("Validation failed! Aborting Pipeline.. ❌")
    else:
        st.sidebar.success("Tables Inserted 🎯")
    return pg_success_tables


def main(base_data_path: PosixPath) -> None:
    st.set_page_config(
        page_title="Pipeline",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.markdown("# Overview")
    st.sidebar.write("This section allows you to trigger the data pipeline.")
    st.sidebar.markdown(
        "You can start the flow selecting **Valid / Invalid** data contracts."
    )
    valid_data_flag = st.sidebar.radio(
        label="Data Contract Type", options=["Valid", "Invalid"], key=500
    )
    local_files_path = list(base_data_path.glob(f"{valid_data_flag.lower()}/*.csv"))
    st.header("Data Pipeline Flow", divider="rainbow")
    if st.sidebar.button(label="Trigger Pipeline 🚀", use_container_width=True):
        upload_success_tables = upload_to_s3(local_files_path)
        pydantic_success_tables = validate_data(upload_success_tables)
        pg_success_tables = insert_to_database(pydantic_success_tables)


if __name__ == "__main__":
    base_data_path = Path.cwd().parent / "data"
    main(base_data_path)
