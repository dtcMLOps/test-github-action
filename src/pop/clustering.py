"""Clustering.py.

This module contains the ClusterEstimatorKMeans class which acts as a concrete ClusterEstimator
class for estimating clusters using KMeans.

Classes:
ClusterEstimatorKMeans: A concrete ClusterEstimator class for estimating clusters using KMeans.

"""
import pyspark.sql
from pop.utils import config
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler


class ClusterEstimatorKMeans:
    """ClusterEstimatorKMeans class.

    The ClusterEstimatorKMeans class acts as a concrete ClusterEstimator class
    for estimating clusters using KMeans. This allows a client application to
    easily create ClusterEstimator objects for estimating clusters using KMeans.

    """

    def __init__(
        self,
        config: config.ConfigManagerClusteringKMeans,
    ) -> None:
        self.config_manager = config
        self._assemble = VectorAssembler(
            inputCols=self.config_manager.columns,
            outputCol="features",
        )

    def fit(self, data: pyspark.sql.DataFrame) -> None:
        """fit method.

        Fits the data to the estimator. This method is called by the client
        application.

        Args:
            data (pyspark.sql.DataFrame): A dataframe with the data to fit.

        """
        self._data = self._assemble.transform(data)
        kmeans = KMeans().setK(self.config_manager.num_cluster).setSeed(1)
        self.model = kmeans.fit(self._data)

    def predict(self) -> pyspark.sql.DataFrame:
        """predict method.

        Predicts the clusters for the data. This method is called by the client application.

        Returns:
            pyspark.sql.DataFrame: A dataframe with the predictions.

        """
        return self.model.transform(self._data)
