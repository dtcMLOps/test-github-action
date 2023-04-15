"""Spark.py.

This module contains the SparkDataLoader class which acts as a concrete DataLoader class for
loading data into Spark.

Classes:
SparkDataLoader: A concrete DataLoader class for loading data into Spark.

Functions:
None

"""

import pyspark.sql
from pyspark import SparkConf


class SparkDataLoader:
    """SparkDataLoader class.

    The SparkDataLoader class acts as a concrete DataLoader class for loading
    data into Spark. This allows a client application to easily create
    DataLoader objects for loading data into Spark.

    """

    def __init__(self, app_name: str):
        conf: SparkConf = SparkConf().setAppName(app_name)
        self.spark_session: pyspark.sql.SparkSession = pyspark.sql.SparkSession.builder.config(
            conf=conf
        ).getOrCreate()

    def read_from_table(
        self,
        schema_name: str,
        table_name: str,
        catalog_name: str = "hive_metastore",
    ) -> pyspark.sql.DataFrame:
        """read method.

        Reads a Delta Lake table from a given catalog and schema

        Args:
            schema_name (str): The name of the schema where the table is located
            table_name (str): The name of the table to be read
            catalog_name (str): The name of the catalog where the table is located

        Raises:
            ValueError: if the table could not be found in the given catalog and schema

        Returns:
            pyspark.sql.DataFrame: Spark DataFrame if the read was successful

        """
        try:
            spark_dataframe = self.spark_session.read.table(
                f"{catalog_name}.{schema_name}.{table_name}"
            )
        except pyspark.sql.utils.AnalysisException as error_message:
            raise ValueError(
                f"table {table_name} could not be found in {catalog_name}.{schema_name}"
            ) from error_message

        return spark_dataframe
