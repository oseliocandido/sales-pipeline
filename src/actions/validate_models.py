from pathlib import PosixPath
import pandas as pd
from pydantic import ValidationError
from typing import List
from models.models import Target
from models.models import Products
from models.models import SalesOrder
from models.models import SalesPerson
from models.models import Sales
from utils.logger import logger


CLASS_MAP = {
    "Target": Target,
    "Products": Products,
    "Sales": Sales,
    "SalesPerson": SalesPerson,
    "SalesOrder": SalesOrder,
}


def validate_model(path: PosixPath) -> List[str]:
    row_error = False
    target_class = CLASS_MAP[path.stem]

    for _, row in pd.read_csv(
        path, delimiter="\t", engine="pyarrow", quotechar='"'
    ).iterrows():
        try:
            target_class(**row.to_dict())
        except ValidationError as error:
            row_error = True
            logger.error(error)
    return row_error
