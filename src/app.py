import streamlit as st
from pathlib import Path
from views.views import pydantic_view
from views.views import upload_s3_view
from views.views import transformation_to_postgres_view


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
    st.sidebar.write("Building....")
    valid_data_flag = st.sidebar.radio(
        label="Data Contract Type", options=["Valid", "Invalid"], key=500
    )

    # Local Path File
    base_data_path = Path.cwd().parent / "data"
    local_files_path = list(
        base_data_path.glob(f"{valid_data_flag.lower()}/Target.csv")
    )
    error_table = True
    # App Flow
    upload_s3_error = upload_s3_view(local_files_path)
    if not upload_s3_error:
        st.sidebar.success("Upload to S3 🚀")
        pydantic_error = pydantic_view(local_files_path)
        if not pydantic_error:
            st.sidebar.success("Data Contract 🚀")
            pg_transformation_error = transformation_to_postgres_view(local_files_path)
            if not pg_transformation_error:
                st.sidebar.success("Tables Inserted with success 🚀")
                # dbt_status = dbt_view(local_files_path)
                # if not dbt_status:
                #     st.sidebar.success('Dbt run with sucess 🚀')
                #     creating_dash = dasboard_view(local_files_path)
                # else:
                #     st.sidebar.error("Error running dbt! Aborting Pipeline... ❌")
                #     st.stop()
            else:
                st.sidebar.error(
                    "Error inserting rows to tables ! Aborting Pipeline... ❌"
                )
                st.stop()
        else:
            st.sidebar.error("Validation failed! Aborting Pipeline... ❌")
            st.stop()
    else:
        st.sidebar.error("Uploaded failed! Aborting Pipeline... ❌")
        st.stop()


if __name__ == "__main__":
    main()


# with st.expander(label='Running dbt....', expanded=True):
#     with st.spinner(text='Running pipeline...'):
#         response = call_dbt()
#         st.code(response,language='bash')

# with st.expander(label='Downloading to S3...', expanded=True):
#     #donwload_s3
#     with st.spinner(text='Validating files'):
#         time.sleep(3)
#         for file in files:
#                 validation_errors = validate.validate_model(file)
#                 if not validation_errors:
#                     st.success(f'{file.stem} ✅')
#                 else:
#                     for error in validation_errors:
#                         st.error(error)

# with st.expander(label='Running DBT...', expanded=True):
#     pass
#     #Running DBT


# with st.container(border=True):
#    st.write("This is inside the container")

#    # You can call any Streamlit command, including custom components:
#    st.bar_chart(np.random.randn(50, 3))


# Report
# with st.container(border=True):
#    st.write("This is inside the container")

#    # You can call any Streamlit command, including custom components:
#    st.bar_chart(np.random.randn(50, 3))


# with st.sidebar:
#     # with st.echo():
#     #     st.write("This code will be printed to the sidebar.")

#     with st.spinner("Loading..."):
#         time.sleep(1)
#     st.success("Done!")

# if st.button(label="Upload s3"):
#     with st.spinner("Uploading to s3..."):
#         status = upload_s3(
#             file_name=path,
#             bucket=config["BUCKET"],
#             key=f"{year}/{month}/{day}/{path.name}",
#         )
#         if status:
#             st.success("Arquivo upado com sucesso")
#         else:
#             st.error("Deu ruim")

# Download from S3 and render in memory
# if st.button("Download from S3"):
#     with st.spinner("Downloading from S3..."):
#         file_downloaded = download_s3(config["BUCKET"], "2024/05/17/Product.csv")

#     if file_downloaded:
#         st.success("Download successful!")
#         with st.spinner("Rendering...."):
#             s3_data = file_downloaded
#             s3_data.seek(0)
#             df = pd.read_csv(s3_data, engine="pyarrow", delimiter="\t")
#             st.dataframe(df)
#     else:
#         st.error("Download failed. Check logs for details.")

# if status == 1:
#     pathzinho = 'asasasas'
#     with st.sidebar:
#         with st.spinner(text='Gererating Data...'):
#             time.sleep(3)
#         st.sidebar.success(f'Data Generated to {pathzinho}')

# col3, col4 = st.columns(2)
# # Add containers to the first column
# with col3:
#     container_1 = st.container()
# # Add containers to the second column
# with col4:
#     container_2 = st.container()
# Laembaixo colocar tecnologias, etc
# st.header('Architecture Pic maybe')
# This work as expected!
# def teste(coluna):
#     return coluna
# b = teste(col5)
# with b:
#     st.write('kkka')
# def write_to_container(container_name) -> None:
#     pass
