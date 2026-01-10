import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException

load_dotenv()


class DataIngestion:
    def __init__(self):
        try:
            self.db_server = os.getenv("DB_SERVER")
            self.db_database = os.getenv("DB_DATABASE")
            self.db_driver = os.getenv("DB_DRIVER")
            self.table_name = os.getenv("TABLE_NAME")

            if not all([self.db_server, self.db_database, self.db_driver, self.table_name]):
                raise ValueError(
                    "Missing DB environment variables. "
                    "Check DB_SERVER, DB_DATABASE, DB_DRIVER, TABLE_NAME in .env"
                )

            self.database_url = (
                f"mssql+pyodbc://@{self.db_server}/{self.db_database}"
                f"?driver={self.db_driver.replace(' ', '+')}"
                f"&trusted_connection=yes"
            )

            logger.info("Database connection initialized")

        except Exception as e:
            logger.exception("Error initializing DataIngestion")
            raise CustomException(e, sys)

    def load_data(self) -> pd.DataFrame:
        try:
            engine = create_engine(self.database_url)
            query = f"SELECT * FROM {self.table_name}"
            df = pd.read_sql(query, engine)

            logger.info("Data loaded successfully from MSSQL")
            return df

        except Exception as e:
            logger.exception("Error loading data from MSSQL")
            raise CustomException(e, sys)
