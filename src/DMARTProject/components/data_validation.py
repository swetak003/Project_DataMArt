import os
import sys
import pandas as pd
from dataclasses import dataclass

from src.DMARTProject.loggers.logger import logger
from src.exception import CustomException

print(">>> RUNNING LATEST DATA_VALIDATION.PY <<<")


@dataclass
class DataValidationConfig:
    raw_data_path: str = "artifacts/raw_data.csv"
    validated_data_dir: str = "artifacts/validated"
    validated_data_path: str = "artifacts/validated/validated_data.csv"


class DataValidation:
    def __init__(self, config: DataValidationConfig = DataValidationConfig()):
        self.config = config

    def validate(self) -> pd.DataFrame:
        """
        Runs data validation checks.
        Allows business-approved nulls in Discount & Profit.
        """
        try:
            logger.info("Starting data validation")

            # -----------------------------
            # Read raw data
            # -----------------------------
            if not os.path.exists(self.config.raw_data_path):
                raise FileNotFoundError("Raw data file not found")

            df = pd.read_csv(self.config.raw_data_path)
            logger.info(f"Raw data loaded. Shape: {df.shape}")

            # -----------------------------
            # 1. Schema validation
            # -----------------------------
            expected_columns = {
                "SalesID",
                "OrderID",
                "OrderDate",
                "ProductID",
                "CustomerID",
                "RegionID",
                "ShipMode",
                "Quantity",
                "Discount",
                "SalesAmount",
                "Profit",
                "LocationID",
                "FeedbackProvided"
            }

            actual_columns = set(df.columns)

            missing_cols = expected_columns - actual_columns
            extra_cols = actual_columns - expected_columns

            if missing_cols:
                raise ValueError(f"Missing columns: {missing_cols}")

            if extra_cols:
                raise ValueError(f"Unexpected columns: {extra_cols}")

            logger.info("Schema validation passed")

            # -----------------------------
            # 2. Null validation (BUSINESS-AWARE)
            # -----------------------------
            allowed_nulls = {"Discount", "Profit"}

            null_counts = df.isna().sum()

            invalid_nulls = {
                col: cnt for col, cnt in null_counts.items()
                if cnt > 0 and col not in allowed_nulls
            }

            if invalid_nulls:
                raise ValueError(f"Unexpected nulls found: {invalid_nulls}")

            logger.info("Null validation passed (business-aware)")

            # -----------------------------
            # 3. Datatype validation
            # -----------------------------
            df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="raise")

            numeric_columns = [
                "Quantity",
                "Discount",
                "SalesAmount",
                "Profit"
            ]

            for col in numeric_columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    raise TypeError(f"{col} must be numeric")

            if not pd.api.types.is_bool_dtype(df["FeedbackProvided"]):
                raise TypeError("FeedbackProvided must be boolean")

            logger.info("Datatype validation passed")

            # -----------------------------
            # 4. Business rule validation
            # -----------------------------
            if (df["Quantity"] <= 0).any():
                raise ValueError("Quantity must be greater than 0")

            if not ((df["Discount"].dropna() >= 0) & (df["Discount"].dropna() <= 1)).all():
                raise ValueError("Discount must be between 0 and 1")

            if (df["SalesAmount"] <= 0).any():
                raise ValueError("SalesAmount must be greater than 0")

            # Profit CAN be negative (losses allowed)
            logger.info("Business rule validation passed")

            # -----------------------------
            # Save validated data
            # -----------------------------
            os.makedirs(self.config.validated_data_dir, exist_ok=True)
            df.to_csv(self.config.validated_data_path, index=False)

            logger.info(
                f"Validated data saved at {self.config.validated_data_path}"
            )

            logger.info("Data validation completed successfully")
            return df

        except Exception as e:
            logger.exception("Data validation failed")
            raise CustomException(e, sys)
