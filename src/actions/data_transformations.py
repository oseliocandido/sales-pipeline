from typing import Callable
import pandas as pd
from sqlalchemy import create_engine
from pathlib import PosixPath
from dotenv import dotenv_values
from utils.logger import logger


class TableTransformer:
    @staticmethod
    def transform_target_table(dataframe):
        # Specific transformations for the Target table
        dataframe["TargetMonth"] = pd.to_datetime(
            dataframe["TargetMonth"], format="%A, %B %d, %Y"
        )
        dataframe["Target"] = (
            dataframe["Target"].replace({"\\$": "", ",": ""}, regex=True).astype(float)
        )
        dataframe.rename(
            columns={
                "EmployeeID": "employeeid",
                "Target": "target",
                "TargetMonth": "targetmonth",
            },
            inplace=True,
        )
        return dataframe

    @staticmethod
    def transform_products_table(dataframe):
        # Specific transformations for the Products table
        return dataframe

    @staticmethod
    def transform(name: str) -> Callable[[pd.DataFrame], pd.DataFrame]:
        if name == "target":
            return TableTransformer.transform_target_table
        elif name == "products":
            return TableTransformer.transform_products_table


class TableProcessor:
    def __init__(self, path: PosixPath):
        env_vars = dotenv_values("../.env")
        db_username = env_vars["DB_USERNAME"]
        db_password = env_vars["POSTGRES_PASSWORD"]
        db_host = env_vars["DB_HOST"]
        db_port = env_vars["DB_PORT"]
        db_name = env_vars["DB_NAME"]
        db_url = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(db_url)

        self.data = path
        self.name = path.stem.lower()

    def run_pipeline(self) -> int | None:
        dataframe = pd.read_csv(
            self.data, engine="pyarrow", quotechar='"', delimiter="\t"
        )
        try:
            transform_function = TableTransformer.transform(self.name)
            transformed_data = transform_function(dataframe)
            rows = transformed_data.to_sql(
                name=self.name,
                if_exists="append",
                con=self.engine,
                method="multi",
                index=False,
            )
        except Exception as error:
            logger.error(error)
            return False
        return rows


# if __name__ == "__main__":
#     path = Path.cwd() / 'data/valid/Target.csv'
#     TableProcessor(path=path).run_pipeline()
