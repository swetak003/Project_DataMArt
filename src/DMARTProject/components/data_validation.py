import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException


@dataclass
class DataValidationConfig:
    raw_data_path: str = "artifacts/raw_data.csv"
    validated_data_dir: str = "artifacts/validated"


class DataValidation:
    def __init__(self, config: DataValidationConfig = DataValidationConfig()):
        self.config = config

    def validate(self) -> pd.DataFrame:
        """
        Read raw data, perform basic validation,
        and save validated data.
        """
        try:
            logger.info(f"Reading raw data from: {self.config.raw_data_path}")

            # Check file exists
            if not os.path.exists(self.config.raw_data_path):
                raise FileNotFoundError(
                    f"File not found: {self.config.raw_data_path}"
                )

            # Read data
            df = pd.read_csv(self.config.raw_data_path)
            logger.info(f"Raw data read successfully. Shape: {df.shape}")

            # Check data not empty
            if df.empty:
                raise ValueError("The raw data file is empty.")

            # Create validated folder
            os.makedirs(self.config.validated_data_dir, exist_ok=True)

            validated_path = os.path.join(
                self.config.validated_data_dir,
                "validated_data.csv"
            )

            # Save validated data
            df.to_csv(validated_path, index=False)
            logger.info(f"Validated data saved at: {validated_path}")

            return df   # ✅ return ONLY at the end

        except Exception as e:
            logger.exception("Data validation failed")
            raise CustomException(e, sys)
