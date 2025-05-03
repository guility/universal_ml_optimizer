import pytest
import pandas as pd
import polars as pl

from utils.df_validator import DataFrameValidator
from errors import MissingFeatureError, NAError


@pytest.fixture
def required_columns():
    return ["col1", "col2", "col3"]


# --- Тесты для pandas DataFrame ---


def test_pandas_valid_df(required_columns):
    df = pd.DataFrame({
        "col1": [1, 2],
        "col2": [3, 4],
        "col3": [5, 6],
    })
    validator = DataFrameValidator(required_columns)
    # Не должно выбрасывать исключений
    validator(df)


def test_pandas_missing_columns(required_columns):
    df = pd.DataFrame({
        "col1": [1, 2],
        "col3": [5, 6],
    })
    validator = DataFrameValidator(required_columns)
    with pytest.raises(MissingFeatureError) as excinfo:
        validator(df)
    missing = excinfo.value.args[0]
    assert "col2" in missing
    assert isinstance(missing, list)


def test_pandas_na_values(required_columns):
    df = pd.DataFrame({
        "col1": [1, None],
        "col2": [3, 4],
        "col3": [5, 6],
    })
    validator = DataFrameValidator(required_columns)
    with pytest.raises(NAError) as excinfo:
        validator(df)
    na_columns, na_number = excinfo.value.args
    assert "col1" in na_columns
    assert na_number == 1


# --- Тесты для polars DataFrame ---


def test_polars_valid_df(required_columns):
    df = pl.DataFrame({
        "col1": [1, 2],
        "col2": [3, 4],
        "col3": [5, 6],
    })
    validator = DataFrameValidator(required_columns)
    validator(df)  # не должно выбрасывать исключений


def test_polars_missing_columns(required_columns):
    df = pl.DataFrame({
        "col1": [1, 2],
        "col3": [5, 6],
    })
    validator = DataFrameValidator(required_columns)
    with pytest.raises(MissingFeatureError) as excinfo:
        validator(df)
    missing = excinfo.value.args[0]
    assert "col2" in missing
    assert isinstance(missing, list)


def test_polars_na_values(required_columns):
    df = pl.DataFrame({
        "col1": [1, None],
        "col2": [3, 4],
        "col3": [5, 6],
    })
    validator = DataFrameValidator(required_columns)
    with pytest.raises(NAError) as excinfo:
        validator(df)
    na_columns, na_number = excinfo.value.args
    assert "col1" in na_columns
    assert na_number == 1


# --- Тест на неподдерживаемый тип ---


def test_invalid_type(required_columns):
    validator = DataFrameValidator(required_columns)
    with pytest.raises(TypeError):
        validator("not a dataframe")