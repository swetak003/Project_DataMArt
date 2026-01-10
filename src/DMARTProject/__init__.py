import os
import sys
from src.DMARTProject.loggers import logger
from src.exception import CustomException
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()###loading environment variables from .env file



class DataIngestion:
    def __init__(self):
        try:
            self.db_server = os.getenv("DB_SERVER")
            self.db_database = os.getenv("DB_DATABASE")
            self.db_driver = os.getenv("DB_DRIVER")
            self.table_name = os.getenv("TABLE_NAME")

            self.database_url = (
                f"mssql+pyodbc://@{self.db_server}/{self.db_database}"
                f"?driver={self.db_driver.replace(' ', '+')}"
                f"&trusted_connection=yes"
            )

        except Exception as e:
            logger.error("Error occurred while initializing DataIngestion class")
            raise CustomException(e, sys)

    def load_data(self) -> pd.DataFrame:
        """Load data from MSSQL database into a pandas DataFrame."""
        try:
            engine = create_engine(self.database_url)
            query = f"SELECT * FROM {self.table_name}"
            df = pd.read_sql(query, engine)
            logger.info("Data loaded successfully from MSSQL database")
            return df

        except Exception as e:
            logger.error("Error occurred while loading data from MSSQL database")
            raise CustomException(e, sys)

    