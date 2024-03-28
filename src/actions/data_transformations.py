from typing import Callable
import pandas as pd
from sqlalchemy import create_engine
from pathlib import PosixPath
from dotenv import dotenv_values
from utils.logger import logger
from pathlib import Path


class TableTransformer:
    @staticmethod
    def transform_target_table(df: pd.DataFrame) -> pd.DataFrame:
        df["TargetMonth"] = pd.to_datetime(df["TargetMonth"], format="%A, %B %d, %Y")
        df["Target"] = (
            df["Target"].replace({"\\$": "", ",": ""}, regex=True).astype(float)
        )
        df.rename(columns=lambda x: x.lower(), inplace=True)
        return df

    @staticmethod
    def transform_products_table(df: pd.DataFrame) -> pd.DataFrame:
        df["Category"] = df["Category"].str.replace("Acessory", "Acessories")
        df["Standard Cost"] = (
            df["Standard Cost"].str.replace("$", "").str.replace(",", "").astype(float)
        )
        df.drop(columns=["Font Color Format"], inplace=True)
        df.rename(columns=lambda x: x.replace(" ", "").lower(), inplace=True)
        return df

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


# Testing
# if __name__ == "__main__":
#     path = Path.cwd().parent / 'data/valid/Target.csv'
#     TableProcessor(path=path).run_pipeline()
