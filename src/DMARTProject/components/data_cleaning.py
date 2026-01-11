import pandas as pd

class DataCleaning:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def clean_data(self) -> pd.DataFrame:
        """
        Performs data cleaning and basic sanity checks.
        No outlier handling or feature engineering here.
        """
        ## Checking the no of rows and columns
        print(f"Initial data shape: {self.df.shape}")
        # -------------------------
        # Missing Value Handling
        # -------------------------
        # Discount missing → no discount applied
        self.df["Discount"] = self.df["Discount"].fillna(0)

        # Profit missing → calculation missing / no profit recorded
        self.df["Profit"] = self.df["Profit"].fillna(0)

        # -------------------------
        # Date Handling
        # -------------------------
        if "OrderDate" in self.df.columns:
            self.df["OrderDate"] = pd.to_datetime(
                self.df["OrderDate"], errors="coerce"
            )

        # -------------------------
        # Remove duplicates
        # -------------------------
        self.df = self.df.drop_duplicates()

        # -------------------------
        # Business sanity rules
        # -------------------------
        self.df = self.df[self.df["Quantity"] > 0]
        self.df = self.df[self.df["SalesAmount"] > 0]
        self.df = self.df[
            (self.df["Discount"] >= 0) & (self.df["Discount"] <= 1)
        ]

        # -------------------------
        # Data type enforcement
        # -------------------------
        id_columns = [col for col in self.df.columns if "ID" in col]
        for col in id_columns:
            self.df[col] = self.df[col].astype("category")

        self.df["ShipMode"] = self.df["ShipMode"].astype("category")

        # -------------------------
        # Reset index
        # -------------------------
        self.df = self.df.reset_index(drop=True)

        return self.df
