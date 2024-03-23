import subprocess
from colorama import init, Fore, Style
import streamlit as st
import re


def call_dbt() -> None:
    # Specify the path to your dbt project folder
    dbt_project_folder = "tasks/dbt/postgres_demo/"

    # Execute the dbt command inside the dbt project folder
    process = subprocess.run(
        "dbt run --select my_first_dbt_model",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=dbt_project_folder,
    )

    # Print the output
    # print("Stdout:", process.stdout.decode())
    # print("Stderr:", process.stderr.decode())
    pattern = re.compile(r"d{2}:d{2}:d{2}")
    # # Print the exit code
    # print("Exit code:", process.returncode)
    # return  process.stdout
    output_str = process.stdout.decode("utf-8")
    color_mapping = {
        "\x1b[32m": "",  # Green
        "\x1b[34m": Fore.BLUE,  # Blue
        "\x1b[0m": "",  # Reset to default color
        "\x1b[39m": Fore.BLACK,
        "\x1b[30m": "",
    }
    st.write(output_str)
    results = re.findall(pattern=pattern, string=output_str)
    st.write(results)
    # Replace ANSI escape codes with colorama styles
    # for code, color_style in color_mapping.items():
    #     output_str = output_str.replace(code, color_style)

    return output_str
    # $value = process.stdout.decode('utf-8')
    # return value.replace("\x1b[32m", Fore.GREEN).replace("\x1b[34m", Fore.BLUE).replace("\x1b[0m",Fore.RESET).replace("\x1b[39m",Fore.RESET)
    # b"\x1b[0m20:03:44  Running with dbt=1.7.10\n\x1b[0m20:03:44  Registered adapter: postgres=1.7.10\n\x1b[0m20:03:44  Found 2 models, 4 tests, 0 sources, 0 exposures, 0 metrics, 401 macros, 0 groups, 0 semantic models\n\x1b[0m20:03:44  \n\x1b[0m20:03:45  Concurrency: 2 threads (target='dev')\n\x1b[0m20:03:45  \n\x1b[0m20:03:45  1 of 1 START sql table model public.my_first_dbt_model ......................... [RUN]\n\x1b[0m20:03:45  1 of 1 OK created sql table model public.my_first_dbt_model .................... [\x1b[32mSELECT 2\x1b[0m in 0.16s]\n\x1b[0m20:03:45  \n\x1b[0m20:03:45  Finished running 1 table model in 0 hours 0 minutes and 0.27 seconds (0.27s).\n\x1b[0m20:03:45  \n\x1b[0m20:03:45  \x1b[32mCompleted successfully\x1b[0m\n\x1b[0m20:03:45  \n\x1b[0m20:03:45  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1\n"``
