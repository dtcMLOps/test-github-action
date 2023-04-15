"""Conftest.py.

This module contains the fixtures for the tests.

fixtures:
    new_table_sales: Fixture to create a new table sales.

"""

import typing
from types import ModuleType

import pytest
from _pytest.main import Session
from pop.utils import config
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType, StructField, StructType


def pytest_sessionstart(session: Session) -> None:
    """pytest_sessionstart.

    Function to create a spark session and set the log level to ERROR before the tests.
    Called after the Session object has been created and before performing collection and
    entering the run test loop.

    https://docs.pytest.org/en/latest/reference/reference.html#pytest.hookspec.pytest_sessionstart

    Args:
        session (Session): session object.

    """
    print()
    spark_session = (
        SparkSession.builder.master("local[1]")
        .appName("local-tests")
        .config("spark.executor.cores", "1")
        .config("spark.executor.instances", "1")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark_session.sparkContext.setLogLevel("ERROR")
    print()


@pytest.fixture(scope="session")
def spark_session() -> typing.Generator[SparkSession, None, None]:
    """spark_session.

    fixture to create a spark session.

    Yields:
        SparkSession: session.

    """

    spark_session = SparkSession.builder.master("local[1]").getOrCreate()

    yield spark_session

    spark_session.stop()


@pytest.fixture(scope="function")
def new_table_sales(spark_session: typing.Annotated[SparkSession, pytest.fixture]) -> DataFrame:
    """New_table_sales.

    fixture to create a new table sales.

    Args:
        spark_session (SparkSession): SparkSession object.

    Returns:
        DataFrame: new table sales.

    """

    data = [
        (
            "400088500",
            "2022-01-31 19:00:00",
            "Corona Extra",
            "Bote 710",
            "0.3407",
        ),
        ("100325192", "2022-02-31 19:00:00", "NPV", "1 L", "0.3600"),
        ("400012860", "2022-03-31 19:00:00", "Bud Light", "Bote", "18.744"),
        (
            "100800911",
            "2022-04-31 19:00:00",
            "Modelo Especial",
            "Laton",
            "1.134",
        ),
        ("100316668", "2022-05-31 19:00:00", "Jugos", "625 ML", "0.225"),
    ]

    schema = StructType(
        [
            StructField("poc_id", StringType(), True),
            StructField("month", StringType(), True),
            StructField("brand", StringType(), True),
            StructField("size", StringType(), True),
            StructField("volume", StringType(), True),
        ]
    )

    df = spark_session.createDataFrame(data=data, schema=schema)
    return df


@pytest.fixture(scope="function")
def new_table_initiatives(
    spark_session: typing.Annotated[SparkSession, pytest.fixture]
) -> DataFrame:
    """New_table_sales.

    fixture to create a new table sales.

    Args:
        spark_session (SparkSession): SparkSession object.

    Returns:
        DataFrame: new table sales.

    """

    data = [
        ("400088500", "Corona Extra_Bote 710", "SUSTAIN"),
        ("100325192", "NPV_1 L", "SUSTAIN"),
        ("400012860", "Bud Light_Bote", "SUSTAIN"),
        ("100800911", "Modelo Especial_Laton", "SUSTAIN"),
        ("100316668", "Jugos_625 ML", "SUSTAIN"),
        ("400088500", "Corona Extra", "SUSTAIN"),
        ("100325192", "NPV", "SUSTAIN"),
        ("400012860", "Bud Light", "SUSTAIN"),
        ("100800911", "Modelo Especial", "SUSTAIN"),
        ("100316668", "Jugos", "SUSTAIN"),
    ]

    schema = StructType(
        [
            StructField("poc_id", StringType(), True),
            StructField("brand", StringType(), True),
            StructField("num_months", StringType(), True),
        ]
    )

    df = spark_session.createDataFrame(data=data, schema=schema)
    return df


@pytest.fixture(scope="function")
def get_config() -> ModuleType:
    """Get_config.

    fixture to get the configuration.

    Returns:
        ModuleType: configuration.

    """
    return config
