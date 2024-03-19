from pathlib import PosixPath
import pandas as pd
from pydantic import ValidationError
from typing import List
from validations.models import Target
from validations.models import Products
from validations.models import SalesOrder


CLASS_MAP = {"Target": Target, "Products": Products, "Sales": SalesOrder}


def validate_model(path: PosixPath) -> List[str]:
    errors = []
    target_class = CLASS_MAP[path.stem]

    # Remove columns after is loaded in database and do there some filtering
    for index, row in pd.read_csv(path, delimiter="\t", engine="pyarrow").iterrows():
        try:
            target_class(**row.to_dict())
        except ValidationError as error_message:
            errors.append(f"{error_message} line {index}")
    return errors


# bota isso pro arquivo de logs mostrando a linhaa
# for error in validation_errors:
#                 st.error(e)
