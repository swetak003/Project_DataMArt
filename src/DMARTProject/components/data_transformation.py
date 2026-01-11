import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException


@dataclass
class DataTransformationConfig:
    validated_data_path: str = "artifacts/validated/validated_data.csv"
    transformed_data_dir: str = "artifacts/transformed"
    transformed_data_path: str = "artifacts/transformed/transformed_data.csv"


class DataTransformation:
    def __init__(self, config: DataTransformationConfig = DataTransformationConfig()):
        self.config = config

    def transform(self) -> pd.DataFrame:
        try:
            logger.info("Starting data transformation")

            # Read validated data
            df = pd.read_csv(self.config.validated_data_path)
            logger.info(f"Validated data loaded. Shape: {df.shape}")

            # -------------------------
            # 1. Handle missing values
            # -------------------------
            df.isnable().sum()
            df["Discount"] = df["Discount"].fillna(0)
            df["Profit"] = df["Profit"].fillna(0)
            logger.info("Missing values handled")

            # -------------------------
            # 2. Convert date columns
            # -------------------------
            if "OrderDate" in df.columns:
                df["OrderDate"] = pd.to_datetime(df["OrderDate"])
                logger.info("OrderDate converted to datetime")

            # -------------------------
            # 3. Encode boolean columns
            # -------------------------
            bool_cols = df.select_dtypes(include="bool").columns
            for col in bool_cols:
                df[col] = df[col].astype(int)
            logger.info("Boolean columns encoded")

            # -------------------------
            # Save transformed data
            # -------------------------
            os.makedirs(self.config.transformed_data_dir, exist_ok=True)
            df.to_csv(self.config.transformed_data_path, index=False)

            logger.info(
                f"Transformed data saved at {self.config.transformed_data_path}"
            )

            return df

        except Exception as e:
            logger.exception("Data transformation failed")
            raise CustomException(e, sys)
