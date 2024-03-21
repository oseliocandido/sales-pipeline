from pathlib import PosixPath
import pandas as pd
from pydantic import ValidationError
from typing import List
from validations.models import Target
from validations.models import Products
from validations.models import SalesOrder
from validations.models import SalesPerson
from validations.models import Sales

import streamlit as st

CLASS_MAP = {
    "Target": Target,
    "Products": Products,
    "Sales": Sales,
    "SalesPerson": SalesPerson,
    "SalesOrder": SalesOrder,
}


def validate_model(path: PosixPath) -> List[str]:
    errors = []
    target_class = CLASS_MAP[path.stem]
    # Remove columns after is loaded in database and do there some filtering
    for _, row in pd.read_csv(
        path, delimiter="\t", engine="pyarrow", quotechar='"'
    ).iterrows():
        try:
            target_class(**row.to_dict())
        except ValidationError:
            errors.append(1)
            break
    return errors


# bota isso pro arquivo de logs mostrando a linhaa
# for error in validation_errors:
# errors.append(f"{error_message} line {index}")
