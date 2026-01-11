from src.DMARTProject.components.data_ingestion_pipeline import DataIngestionPipeline
from src.DMARTProject.components.data_validation import DataValidation
from src.DMARTProject.loggers.logger import logger
#from src.DMARTProject.components.data_transformation import DataTransformation
from src.DMARTProject.components.data_cleaning import DataCleaning
from src.DMARTProject.components.data_analysis import DataAnalysis
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
        # STEP 3: DATA CLEANING
        cleaner=DataCleaning(validated_df)
        cleaned_df=cleaner.clean_data()
        logger.info("Data Cleaning Completed")

        ### step 4: DATA ANALYSIS
        analyzer=DataAnalysis(cleaned_df)
        logger.info(f"EDA Summary: {analyzer.basic_metrics()}")
        #analyzer.generate_reports()
        analyzer.numerical_summary()
        analyzer.save_core_plots()
        logger.info("EDA artifacts saved")
        
        logger.info("Data Analysis Completed")     
        
        
        
        
        
        #STEP 3: Trasformation
        # tranformer=DataTransformation()
        # tranformer.transform()
        # logger.info("Data Transformation Completed")

    except Exception as e:
        logger.exception("Application failed")
        raise CustomException(e, sys)
