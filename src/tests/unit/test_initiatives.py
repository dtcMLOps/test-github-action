"""test_initiatives.

Test the initiatives module.

Functions:
    test_table_initiatives_with_end_date_last_months: Test that the table initiatives properties
                                                      are calculated correctly when start and
                                                      end date are provided.
    test_table_initiatives_with_end_date_last_months: Test that the table initiatives properties
                                                      are calculated correctly when start and
                                                      end date are provided.

"""
import datetime
import typing

import pytest
from pop import initiatives
from pop.utils import config
from pyspark.sql import DataFrame, SparkSession

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


@pytest.mark.parametrize(
    "arg,expected",
    [
        (
            {"end_date": "2022-02-01", "last_months": 2},
            pytest.lazy_fixture("new_table_initiatives"),
        ),
        (
            {"start_date": "2022-01-01", "end_date": "2022-02-01"},
            pytest.lazy_fixture("new_table_initiatives"),
        ),
    ],
    ids=["end_date-last_months", "start_date-end_date"],
)
def test_table_initiatives(
    arg: typing.Dict[str, typing.Union[str, int]],
    expected: typing.Annotated[DataFrame, pytest.fixture],
    new_table_sales: typing.Annotated[DataFrame, pytest.fixture],
    monkeypatch: typing.Annotated[pytest.MonkeyPatch, pytest.fixture],
    spark_session: typing.Annotated[SparkSession, pytest.fixture],
    get_config: typing.Annotated[config.ConfigManagerInitiatives, pytest.fixture],
):
    """test_table_initiatives_with_end_date_last_months.

    Test that the table initiatives properties are calculated correctly when start and end
    date are provided.

    Args:
        arg (dict): dictionary with the start_date and end_date
        expected (pytest.fixture): expected table initiatives
        new_table_sales (pytest.fixture): pyspark DataFrame with the sales
        monkeypatch (pytest.MonkeyPatch): monkeypatch object
        spark_session (pytest.fixture): spark_session object
        get_config (pytest.fixture): object to get the configuration

    """

    def mockreturn_get_min_max_date(
        self, table: str, column_name: str, end_date: str, last_months: int
    ) -> typing.Tuple[datetime.date, datetime.date]:
        """monkeypatch for get_min_max_date.

        function to monkeypatch get_min_max_date.

        Args:
            self (object): object to monkeypatch
            table (str): table name
            column_name (str): column name
            end_date (str): max date to calculate the potential initiatives
            last_months (int): min date to calculate the potential initiatives

        Returns:
            typing.Tuple[datetime.date, datetime.date]: min and max date to calculate the potential
                                                        initiatives

        """

        return (
            datetime.datetime.strptime("2021-12-01 00:00:00", DATE_FORMAT).date(),
            datetime.datetime.strptime("2022-01-31 23:59:59", DATE_FORMAT).date(),
        )

    def mockreturn_spark_sql(self, query: str) -> DataFrame:
        """monkeypatch for spark sql.

        function to monkeypatch spark sql.

        Args:
            self (object): object to monkeypatch
            query (str): query to execute

        Returns:
            DataFrame: PySpark DataFrame with the potential initiatives.

        """

        return new_table_sales

    monkeypatch.setattr(
        "pop.utils.utils.get_min_max_date",
        mockreturn_get_min_max_date,
    )

    monkeypatch.setattr(
        "pyspark.sql.SparkSession.sql",
        mockreturn_spark_sql,
    )

    # GIVEN a table with sales
    potential_initiatives = initiatives.PotentialInitiatives(spark_session=spark_session)

    # configuration object
    config_manager = get_config.ConfigManagerInitiatives(**arg)

    # WHEN calculate is called
    table_initiatives = potential_initiatives.calculate(config_manager=config_manager)

    # THEN check that the table initiatives properties are calculated correctly
    assert len(table_initiatives.columns) == 3
    assert table_initiatives.count() == 10
    assert table_initiatives.columns == ["poc_id", "brand", "num_months"]
    assert table_initiatives.subtract(expected).count() == 0
