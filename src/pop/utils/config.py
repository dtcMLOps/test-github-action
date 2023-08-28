"""Config for the pop package.

This module contains the configuration for the pop package.

Classes:
    ConfigManagerInitiatives: Config for the ManagerInitiatives class.
    ConfigManagerClusteringKMeans: Config for the ManagerClusteringKMeans class.

"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ConfigManagerInitiatives:
    """Config for the ManagerInitiatives class.

    Class to manage the parameters to calculate the potential initiatives.

    Attributes:

        table_name (str): Table name to calculate the potential initiatives.
        column_name (str): Column name to calculate the potential initiatives.
        start_date (str): Start date to calculate the potential initiatives.
        end_date (str): End date to calculate the potential initiatives.
        last_months (int): Number of months to calculate the potential initiatives.

    """

    table_name: Optional[str] = None
    column_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    last_months: Optional[int] = 2


@dataclass
class ConfigManagerClusteringKMeans:
    """Config for the ManagerClusteringKMeans class.

    Class to manage the parameters to calculate the predictions using KMeans.

    Attributes:

        num_cluster (int): Number of clusters
        columns (List[str]): Columns to calculate the predictions using KMeans.
        poc_id (int): POC id to calculate the predictions using KMeans.

    """

    num_cluster: Optional[int] = 3
    columns: Optional[List[str]] = field(default_factory=list)
    poc_id: Optional[int] = None
