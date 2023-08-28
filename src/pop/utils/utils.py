"""Data utils.

This module contains the utility functions for the data.

"""
import datetime
from calendar import monthrange

import pyspark.sql.functions
from dateutil.relativedelta import relativedelta


def label_map(spark_dataframe, column: str, replace: dict, inplace: bool = False):
    """Label_map.

    Replaces values in given dataframe column by the dictionary.
    By default generates a new column with suffix '_replaced'.

    Args:
        spark_dataframe (pyspark.sql.dataframe.DataFrame): Dataframe to be modified.
        column (str): Column to be modified.
        replace (dict): Dictionary with values to be replaced.
        inplace (bool): If True, replaces the original column. Defaults to False.

    Returns:
        pyspark.sql.dataframe.DataFrame: Dataframe with modified column.

    """
    vals = pyspark.sql.functions.col(column)
    for key_, value_ in replace.items():
        vals = pyspark.sql.functions.regexp_replace(vals, key_, value_)
    if inplace:
        spark_dataframe = spark_dataframe.withColumn(column, vals)
    else:
        new_col = f"{column}_replaced"
        spark_dataframe = spark_dataframe.withColumn(new_col, vals)
    return spark_dataframe


def get_min_max_date(
    spark_session: pyspark.sql.SparkSession,
    table: str,
    column_name: str,
    end_date: str,
    last_months: int,
) -> datetime.datetime:
    """Get min and max date.

    Function to get the min and max date for a given table and column.

    Args:
        spark_session (pyspark.sql.SparkSession): Spark session.
        table (str): table name to get the min and max date.
        column_name (str): column name to get the min and max date.
        end_date (str): end date to define the max date.
        last_months (int): number of months to define the min date.

    Returns:
        datetime.datetime: min and max date.

    """

    end_date_for_aggregation = (
        (
            spark_session.sql(f"SELECT MAX(cast({column_name} as DATE)) FROM {table}")
            .toPandas()
            .iloc[0, 0]
        )
        if end_date is None
        else datetime.datetime.combine(
            datetime.datetime.strptime(end_date, "%Y-%m-%d").date(),
            datetime.time.min,
        )
    )
    last_month_day = monthrange(end_date_for_aggregation.year, end_date_for_aggregation.month)[1]
    end_date_for_aggregation = (
        end_date_for_aggregation.replace(day=1) - datetime.timedelta(days=1)
        if end_date_for_aggregation.day != last_month_day
        else end_date_for_aggregation
    )
    end_date_for_aggregation = end_date_for_aggregation.replace(hour=23, minute=59, second=59)
    initial_date_for_aggregation = (
        end_date_for_aggregation.replace(hour=0, minute=0, second=0, day=1)
        - relativedelta(months=last_months - 1)
        if last_months
        else (
            spark_session.sql(f"SELECT MIN(cast({column_name} as DATE)) FROM {table}")
            .toPandas()
            .iloc[0, 0]
        )
    )
    initial_date_for_aggregation = initial_date_for_aggregation.replace(
        hour=0, minute=0, second=0, day=1
    )
    return initial_date_for_aggregation, end_date_for_aggregation
