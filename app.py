from src.DMARTProject.components.data_ingestion_pipeline import DataIngestionPipeline
from src.DMARTProject.components.data_validation import DataValidation
from src.DMARTProject.components.data_cleaning import DataCleaning
from src.DMARTProject.components.data_analysis import DataAnalysis
from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException
from src.DMARTProject.components.datapersistence import DataPersistence


from sqlalchemy import create_engine
import pandas as pd
import sys
import os


DATABASE_URL = (
    "mssql+pyodbc://@DESKTOP-FS7EJOC\\SQLEXPRESS/DMART"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)



if __name__ == "__main__":
    try:
        logger.info("DMART application started")

        # ===============================
        # STEP 1: DATA INGESTION
        # ===============================
        pipeline = DataIngestionPipeline()
        raw_path, train_path, test_path = pipeline.initiate_data_ingestion()
        logger.info("Data ingestion completed")

        # ===============================
        # STEP 2: DATA VALIDATION (CONFIG-DRIVEN)
        # ===============================
        validator = DataValidation()
        validated_df = validator.validate()
        logger.info("Data validation completed")

        # ===============================
        # STEP 3: DATA CLEANING
        # ===============================
        cleaner = DataCleaning(validated_df)
        cleaned_df = cleaner.clean_data()
        logger.info("Data cleaning completed")

        # ===============================
        # STEP 4: DATA ANALYSIS
        # ===============================
        analyzer = DataAnalysis(cleaned_df)
        logger.info(f"EDA Metrics: {analyzer.basic_metrics()}")
        analyzer.save_core_plots()
        logger.info("EDA artifacts saved")

        # ===============================
        # STEP 5: SAVE CLEANED DATA
        # ===============================
        os.makedirs("artifacts", exist_ok=True)
        cleaned_path = "artifacts/cleaned_data.csv"
        cleaned_df.to_csv(cleaned_path, index=False)
        logger.info(f"Cleaned data saved at {cleaned_path}")

        # ===============================
        # STEP 6: WRITE TO SQL
        # ===============================
        persistence = DataPersistence(DATABASE_URL)
        persistence.write_to_sql(cleaned_df, table_name="DMART_Cleaned")
        
        logger.info("Cleaned data written to SQL table")

        logger.info("DMART application finished successfully")

    except Exception as e:
        logger.exception("Application failed")
        raise CustomException(e, sys)
