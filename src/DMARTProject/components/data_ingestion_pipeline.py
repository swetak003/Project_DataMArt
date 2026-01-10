import os
import sys
from src.DMARTProject.components.data_ingestion import DataIngestion
from src.DMARTProject.utils.common import create_directories
from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException
from sklearn.model_selection import train_test_split


class DataIngestionPipeline:
    def initiate_data_ingestion(self):
        try:
            logger.info("Starting Data Ingestion Pipeline")

            # Call your DataIngestion class
            ingestion = DataIngestion()
            df = ingestion.load_data()
            print(df.head())

            # Create artifacts folder
            create_directories("artifacts")

            # Save raw data
            raw_path = os.path.join("artifacts", "raw_data.csv")
            df.to_csv(raw_path, index=False)

            logger.info(f"Raw data saved at {raw_path}")
            logger.info("Data Ingestion Pipeline completed successfully")

            ## Split DAta
            train_df, test_df = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )
            # Save train and test data
            train_path= os.path.join("artifacts", "train_data.csv")
            test_path= os.path.join("artifacts", "test_data.csv")
            
            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)

            logger.info("Train-test split completed successfully")
            logger.info(f"Train data saved at {train_path}")
            logger.info(f"Test data saved at {test_path}")
            return (raw_path, train_path, test_path)
        
        except Exception as e:
            logger.exception("Data Ingestion Pipeline failed")
            raise CustomException(e, sys)
