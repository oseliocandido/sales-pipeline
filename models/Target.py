from pydantic import BaseModel, ValidationError, Field, field_validator
from datetime import datetime
import pandas as pd
from pathlib import Path


class Target(BaseModel):
    EmployeeID: int
    Target: str
    TargetMonth: str

    @field_validator("TargetMonth")
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%A, %B %d, %Y")
        except:
            raise ValueError("Invalid date format")
        return value


path = Path.cwd() / "data" / "Targets.csv"

df = pd.read_csv(path, engine="pyarrow", delimiter="\t")


try:
    for index, row in df.iterrows():
        Target(**row.to_dict())
    print(df.head())
except ValidationError as error:
    print(f"Line {index} has an error")
    print(error)
