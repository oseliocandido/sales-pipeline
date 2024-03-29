import streamlit as st

st.set_page_config(page_title="Logs", page_icon="📜")
st.markdown(
    """
### Logs 
Error messages related to the data pipeline process.
"""
)

log_file_path = "../logs/error.log"
with open(log_file_path, "r") as log_file:
    log_lines = log_file.readlines()
current_error_message = ""
for line in log_lines:
    if "ERROR" in line:
        if current_error_message:
            st.error(current_error_message)
        current_error_message = line.strip()
    elif current_error_message:
        current_error_message += "\n" + line.strip()
if current_error_message:
    st.error(current_error_message)
