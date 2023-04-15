"""Initiatives.py.

This module contains the functions to calculate the potential initiatives for a given table.

Functions:
    potential_initiatives: Function to calculate the potential initiatives for a given table.

"""


import os

import pyspark.sql.functions
from pop.utils import config, sql, utils
from pyspark.sql import DataFrame, SparkSession


class PotentialInitiatives:
    """PotentialInitiatives class.

    Class to calculate the potential initiatives for a given table.
    It will return a table with the potential initiatives.

    Attributes:
        table_name (str): Table name to calculate the potential initiatives.
        start_date (str): Start date to calculate the potential initiatives.
        end_date (str): End date to calculate the potential initiatives.
        last_months (int): Number of months to calculate the potential initiatives.

    """

    def __init__(self, spark_session: SparkSession) -> None:
        self.spark_session: SparkSession = spark_session

    def calculate(self, config_manager: config.ConfigManagerInitiatives) -> DataFrame:
        """Potential_initiatives.

        Function to calculate the potential initiatives for a given table.
        It will return a table with the potential initiatives.

        Args:
            config_manager (ConfigManager): ConfigManager object with the parameters to calculate
                                    the potential initiatives.

        Returns:
            DataFrame: PySpark DataFrame with the potential initiatives.

        """

        # 1. Get start-date and end-date based on input parameters
        if config_manager.start_date and config_manager.end_date:
            initial_date_for_aggregation = config_manager.start_date
            end_date_for_aggregation = config_manager.end_date
        else:
            (initial_date_for_aggregation, end_date_for_aggregation,) = utils.get_min_max_date(
                self.spark_session,
                table=config_manager.table_name,
                column_name=config_manager.column_name,
                end_date=config_manager.end_date,
                last_months=config_manager.last_months,
            )

        query = sql.read_from_sql(
            filename=os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "queries",
                "initiatives.sql",
            ),
            query_parameters={
                "table_name": config_manager.table_name,
                "column_name": "month",
                "initial_date_for_aggregation": initial_date_for_aggregation,
                "end_date_for_aggregation": end_date_for_aggregation,
            },
        )

        # 2. Get table marca-cupo between initial_date_for_aggregation and end_date_for_aggregation
        table_marca_cupo = self.spark_session.sql(query)

        # 3. Get table marca
        table_marca = (
            table_marca_cupo["poc_id", "month", "brand", "volume"]
            .groupby(["poc_id", "month", "brand"])
            .agg(pyspark.sql.functions.sum("volume").alias("volume"))
        )

        # 4. Merge brand and size column
        table_marca_cupo = table_marca_cupo.select(
            "poc_id",
            "month",
            pyspark.sql.functions.concat("brand", pyspark.sql.functions.lit("_"), "size").alias(
                "brand"
            ),
            "volume",
        )

        # 5. Join table marca-cupo and marca
        union_table = table_marca_cupo.unionAll(table_marca)

        # 6. Count distinct months
        final_table = union_table.groupby("poc_id", "brand").agg(
            pyspark.sql.functions.expr("count(distinct month)").cast("string").alias("num_months")
        )

        # 7. Define business rules
        business_rules = {
            "0": "INTRODUCE",
            "1": "SUSTAIN",
            "2": "SUSTAIN",
            "3": "GENERATE",
        }

        # 8. Replace num_months with business rules
        table_initiatives = utils.label_map(
            final_table, column="num_months", replace=business_rules, inplace=True
        )

        return table_initiatives
