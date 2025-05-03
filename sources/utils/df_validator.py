import pandas as pd
import polars as pl

from errors import MissingFeatureError, NAError
from utils.logger import Logger

logger = Logger(__name__)


class DataFrameValidator:
    def __init__(self, required_columns: list[str]):
        self.required_columns = required_columns

    def __call__(self, df: pl.DataFrame | pd.DataFrame):
        if isinstance(df, pd.DataFrame):
            return self.__validate_pandas(df)
        elif isinstance(df, pl.DataFrame):
            return self.__validate_polars(df)
        else:
            raise TypeError(f"Expected pandas of polars DataFrame, but got {type(df)}")

    def __validate_pandas(self, df: pd.DataFrame):
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise MissingFeatureError(missing_cols)
        nas = df.isna()
        if nas.any().any():
            na_number = nas.sum().sum()
            na_columns = df.columns[nas.any(axis=0)].tolist()
            raise NAError(na_columns, na_number)

    def __validate_polars(self, df: pl.DataFrame):
        missing_columns = set(self.required_columns) - set(df.columns)
        if missing_columns:
            missing_columns = [col for col in self.required_columns if col in missing_columns]
            raise MissingFeatureError(missing_columns)

        na_number = df.null_count()
        if na_number:
            na_columns = [col for col in self.required_columns if df[col].null_count() > 0]
            raise NAError(na_columns, na_number)
