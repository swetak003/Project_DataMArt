from src.DMARTProject.loggers.logger import logger  
from src.exception import CustomException
from src.DMARTProject.components.data_ingestion import DataIngestionPipeline
from src.DMARTProject.__init__ import load_dotenv
from src.DMARTProject.components.data_ingestion import DataIngestion

import sys  

if __name__ == "__main__":
    logger.info("DMART Project started successfully.")
    try:
        logger.info("Starting DMART Project application.")
        data_ingestion_pipeline = DataIngestionPipeline()
        data_ingestion_pipeline.initiate_data_ingestion()
        logger.info("DMART Project application finished successfully.")

    # Application logic goes here
    except Exception as e:
        logger.error("An error occurred in DMART Project application.")
        raise CustomException(e, sys)



