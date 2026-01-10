import os
import sys
from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException   
from src.DMARTProject.utils.common import create_directories
from src.DMARTProject.__init__ import DataIngestion
import pandas as pd


from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    raw_data_path: str=os.path.join("artifacts","raw_data.csv")
    train_data_path: str=os.path.join("artifacts","train_data.csv")
    test_data_path: str=os.path.join("artifacts","test_data.csv")
    test_size: float=0.2
    random_state: int=42
class DataIngestionPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

      

    def initiate_data_ingestion(self):
        logger.info("Data Ingestion started")
        try:
            data_ingestion=DataIngestion()
            raw_data_df=data_ingestion.load_data()
            ##reading data from source
            logger.info("Reading from mssql database completed successfully")

            create_directories(os.path.dirname(self.data_ingestion_config.raw_data_path))

            raw_data_df.to_csv(self.data_ingestion_config.raw_data_path,index=False)
            logger.info(f"Raw data saved at {self.data_ingestion_config.raw_data_path}")

            train_df,test_df=data_ingestion.split_data_as_train_test(raw_data_df,
                                                                      test_size=self.data_ingestion_config.test_size,
                                                                      random_state=self.data_ingestion_config.random_state)
            train_df.to_csv(self.data_ingestion_config.train_data_path,index=False)
            test_df.to_csv(self.data_ingestion_config.test_data_path,index=False)
            logger.info("Data ingestion completed successfully")

            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )
        except Exception as e:
            logger.error("Error occurred during data ingestion")
            raise CustomException(e,sys)