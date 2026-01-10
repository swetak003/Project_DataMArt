from src.DMARTProject.components.data_ingestion_pipeline import DataIngestionPipeline
from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException
import sys


if __name__ == "__main__":
    try:
        logger.info("DMART application started")

        pipeline = DataIngestionPipeline()
        pipeline.initiate_data_ingestion()

        logger.info("DMART application finished successfully")

    except Exception as e:
        logger.exception("Application failed")
        raise CustomException(e, sys)
