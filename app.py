from src.DMARTProject.components.data_ingestion_pipeline import DataIngestionPipeline
from src.DMARTProject.components.data_validation import DataValidation
from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException
import sys


if __name__ == "__main__":
    try:
        logger.info("DMART application started")

        # STEP 1: Ingestion
        pipeline = DataIngestionPipeline()
        pipeline.initiate_data_ingestion()
        logger.info("Data ingestion completed")

        # STEP 2: Validation
        validator = DataValidation()
        validated_df = validator.validate()   # ⬅️ capture return
        logger.info("Data validation completed")

        logger.info("DMART application finished successfully")

    except Exception as e:
        logger.exception("Application failed")
        raise CustomException(e, sys)
