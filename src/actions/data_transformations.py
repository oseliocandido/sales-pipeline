from typing import Callable
import pandas as pd
from sqlalchemy import create_engine
from pathlib import PosixPath
from dotenv import dotenv_values
from utils.logger import logger


class TableTransformer:
    @staticmethod
    def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns=lambda x: x.replace(" ", "").lower(), inplace=True)
        return df

    @staticmethod
    def get_transformation_function(
        name: str,
    ) -> Callable[[pd.DataFrame], pd.DataFrame]:
        transformation_functions = {
            "target": TableTransformer.Target,
            "products": TableTransformer.Products,
            "sales": TableTransformer.Sales,
            "salesorder": TableTransformer.SalesOrder,
            "salesperson": TableTransformer.SalesPerson,
        }
        return transformation_functions.get(name)

    @staticmethod
    def Target(df: pd.DataFrame) -> pd.DataFrame:
        df["TargetMonth"] = pd.to_datetime(df["TargetMonth"], format="%A, %B %d, %Y")
        df["Target"] = (
            df["Target"].replace({"\\$": "", ",": ""}, regex=True).astype(float)
        )
        return df

    @staticmethod
    def Products(df: pd.DataFrame) -> pd.DataFrame:
        df["Category"] = df["Category"].str.replace("Acessory", "Acessories")
        df["Standard Cost"] = (
            df["Standard Cost"].str.replace("$", "").str.replace(",", "").astype(float)
        )
        df.drop(columns=["Font Color Format"], inplace=True)
        return df

    @staticmethod
    def Sales(df: pd.DataFrame) -> pd.DataFrame:
        df["Cost"] = df["Cost"].str.replace("$", "").str.replace(",", "").astype(float)
        df["Unit Price"] = (
            df["Unit Price"].str.replace("$", "").str.replace(",", "").astype(float)
        )
        return df

    @staticmethod
    def SalesOrder(df: pd.DataFrame) -> pd.DataFrame:
        df["OrderDate"] = pd.to_datetime(df["OrderDate"], format="%A, %B %d, %Y")
        return df

    @staticmethod
    def SalesPerson(df: pd.DataFrame) -> pd.DataFrame:
        return df


class TableProcessor:
    env_vars = dotenv_values("../.env")
    db_username = env_vars["DB_USERNAME"]
    db_password = env_vars["POSTGRES_PASSWORD"]
    db_host = env_vars["DB_HOST"]
    db_port = env_vars["DB_PORT"]
    db_name = env_vars["DB_NAME"]
    engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    def __init__(self, path: PosixPath):
        self.path = path
        self.name = path.stem.lower()

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.path, engine="pyarrow", quotechar='"', delimiter="\t")

    def run_pipeline(self) -> int | None:
        try:
            dataframe = self.read_csv()
            transform_function = TableTransformer.get_transformation_function(self.name)
            transformed_data = transform_function(dataframe)
            renamed_transformed_data = TableTransformer.rename_columns(transformed_data)
            rows = renamed_transformed_data.to_sql(
                name=self.name,
                if_exists="append",
                con=TableProcessor.engine,
                method="multi",
                index=False,
            )
        except Exception as error:
            logger.error(error)
            return False
        return rows
