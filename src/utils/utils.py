from pathlib import Path, PosixPath
import pandas as pd
from time import perf_counter


def normalize_table(path: PosixPath, engine=str) -> None:
    df = pd.read_csv(filepath_or_buffer=path, delimiter=",", engine=engine)
    new_df = df[["SalesOrderNumber", "ProductKey", "Quantity", "Unit Price"]]
    # distinct_df = new_df.drop_duplicates()
    new_df.to_csv(
        path_or_buf=Path.cwd() / "data/valid/Sales.csv", index=False, sep="\t"
    )


if __name__ == "__main__":
    path = Path.cwd() / "data/valid/Sales.csv"
    # normalize_table(path,'pyarrow')
    normalize_table(path, "python")

# - nan string instead None
# - Additional double quote

# Bronze
# # - Only Accepted Values
# Silver
# # - Unecessary Columns\
#  Upper-LowerCase
# # - string in numeric types and vice versa
# # - Expected this format as string  in timestamp fields
# #   -- Tue Dec 30 2014 12:00:00 GMT-0800 (PST)

# Bronze to silver
# # - Duplicate Primary keys
