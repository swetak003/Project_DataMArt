import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict


class DataAnalysis:
    """
    Enterprise-grade Data Analysis component.
    Performs headless EDA: metrics, summaries, correlations.
    Visualization is optional and saved as artifacts.
    """

    NUMERIC_COLS = ["Quantity", "Discount", "SalesAmount", "Profit"]

    def __init__(self, df: pd.DataFrame, artifact_path: str = "artifacts/eda"):
        self.df = df.copy()
        self.artifact_path = artifact_path
        os.makedirs(self.artifact_path, exist_ok=True)

    # ==========================
    # INTERNAL SAFETY CHECK
    # ==========================
    def _check_columns(self, cols):
        missing = set(cols) - set(self.df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    # ==========================
    # BASIC BUSINESS METRICS
    # ==========================
    def basic_metrics(self) -> Dict:
        self._check_columns(["Profit", "Discount"])

        return {
            "row_count": self.df.shape[0],
            "column_count": self.df.shape[1],
            "loss_rate": round((self.df["Profit"] < 0).mean(), 4),
            "avg_discount": round(self.df["Discount"].mean(), 4),
            "avg_profit": round(self.df["Profit"].mean(), 2),
            "total_profit": round(self.df["Profit"].sum(), 2)
        }

    # ==========================
    # NUMERICAL SUMMARY
    # ==========================
    def numerical_summary(self) -> pd.DataFrame:
        self._check_columns(self.NUMERIC_COLS)
        return self.df[self.NUMERIC_COLS].describe().T

    # ==========================
    # CATEGORICAL DISTRIBUTIONS
    # ==========================
    def categorical_summary(self) -> Dict:
        return {
            "ShipMode": self.df["ShipMode"].value_counts(),
            "FeedbackProvided": self.df["FeedbackProvided"].value_counts(normalize=True)
        }

    # ==========================
    # CORRELATION ANALYSIS
    # ==========================
    def correlation_matrix(self) -> pd.DataFrame:
        self._check_columns(self.NUMERIC_COLS)
        return self.df[self.NUMERIC_COLS].corr()

    # ==========================
    # DISCOUNT IMPACT ANALYSIS
    # ==========================
    def discount_bucket_profit(self) -> pd.DataFrame:
        self._check_columns(["Discount", "Profit"])

        df_temp = self.df.copy()
        df_temp["Discount_Bucket"] = pd.cut(
            df_temp["Discount"],
            bins=[0, 0.1, 0.3, 0.5, 0.75, 1.0],
            labels=["Low", "Medium", "High", "Very_High", "Extreme"]
        )

        return (
            df_temp
            .groupby("Discount_Bucket", observed=True)["Profit"]
            .mean()
            .reset_index()
        )

    # ==========================
    # SAVE EDA PLOTS (OPTIONAL)
    # ==========================
    def save_core_plots(self):
        # Count plots
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        sns.countplot(x="ShipMode", data=self.df, ax=axes[0])
        axes[0].set_title("Ship Mode Counts")

        sns.countplot(x="FeedbackProvided", data=self.df, ax=axes[1])
        axes[1].set_title("Feedback Provided Counts")

        plt.tight_layout()
        plt.savefig(f"{self.artifact_path}/univariate_countplots.png", dpi=300)
        plt.close()

        # Distribution plots
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        sns.histplot(self.df["SalesAmount"], bins=30, kde=True, ax=axes[0])
        axes[0].set_title("Sales Distribution")

        sns.histplot(self.df["Profit"], bins=30, kde=True, ax=axes[1])
        axes[1].set_title("Profit Distribution")

        sns.histplot(self.df["Discount"], bins=30, kde=True, ax=axes[2])
        axes[2].set_title("Discount Distribution")

        plt.tight_layout()
        plt.savefig(f"{self.artifact_path}/univariate_distributions.png", dpi=300)
        plt.close()

        # Correlation heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(self.correlation_matrix(), annot=True, cmap="coolwarm")
        plt.title("Correlation Matrix")
        plt.savefig(f"{self.artifact_path}/correlation_matrix.png", dpi=300)
        plt.close()


    # ==========================


# ====================
#     # BASIC SUMMARY
#     # ==========================
#     def basic_summary(self):
#         """
#         Provides basic summary of the DataFrame including
#         shape, data types, missing values, statistics, and loss rate.
#         """
#         return {
#             "shape": self.df.shape,
#             "data_types": self.df.dtypes,
#             "missing_values": self.df.isna().sum(),
#             "basic_statistics": self.df.describe(),
#             "loss_rate": (self.df["Profit"] < 0).mean()
#         }

#     # ==========================
#     # NUMERICAL SUMMARY
#     # ==========================
#     def generate_summary_statistics(self) -> pd.DataFrame:
#         return self.df.select_dtypes(include=["number"]).describe().T

#     # ==========================
#     # VALUE COUNTS (CATEGORICAL)
#     # ==========================
#     def value_counts_summary(self):
#         return {
#             "ShipMode": self.df["ShipMode"].value_counts(),
#             "FeedbackProvided": self.df["FeedbackProvided"].value_counts(normalize=True)
#         }

#     # ==========================
#     # UNIVARIATE ANALYSIS
#     # ==========================

#     ### DISTRIBUTION PLOTS
#     def plot_distributions(self):
#         fig, axes = plt.subplots(1, 3, figsize=(15, 4))

#         sns.histplot(self.df["SalesAmount"], bins=30, kde=True, ax=axes[0])
#         axes[0].set_title("Sales Amount Distribution")
#         axes[0].grid(True)

#         sns.histplot(self.df["Profit"], bins=30, kde=True, ax=axes[1])
#         axes[1].set_title("Profit Distribution")
#         axes[1].grid(True)

#         sns.histplot(self.df["Discount"], bins=30, kde=True, ax=axes[2])
#         axes[2].set_title("Discount Distribution")
#         axes[2].grid(True)

#         plt.tight_layout()
#         plt.show()
#     ### countplots
#     def plot_countplots(self):
#         fig, axes = plt.subplots(1, 2, figsize=(12, 4))

#         sns.countplot(x="ShipMode", data=self.df, ax=axes[0])
#         axes[0].set_title("Ship Mode Counts")
#         axes[0].grid(True)
#         axes[0].set_xlabel("Ship Mode")
#         axes[0].set_ylabel("Count")
#         axes[0].tick_params(axis='x', rotation=45)
#         axes[0].bar_label(axes[0].containers[0])

#         sns.countplot(x="FeedbackProvided", data=self.df, ax=axes[1])
#         axes[1].set_title("Feedback Provided Counts")
#         axes[1].grid(True)
#         axes[1].set_xlabel("Feedback Provided")
#         axes[1].set_ylabel("Count")
#         axes[1].tick_params(axis='x', rotation=45)
#         axes[1].bar_label(axes[1].containers[0])

#         plt.tight_layout()
#         plt.show()
#     # ==========================
#     # BIVARIATE ANALYSIS
#     # ==========================

#     def plot_bivariate(self):
#         # Sales vs Profit
#         self.df["ProfitStatus"] = self.df["Profit"].apply(
#             lambda x: "Profitable" if x > 0 else "Loss/Break-even"
#         )

#         sns.scatterplot(
#             data=self.df,
#             x="SalesAmount",
#             y="Profit",
#             hue="ProfitStatus",
#             alpha=0.6
#         )
#         plt.title("Sales Amount vs Profit")
#         plt.show()

#         self.df.drop(columns=["ProfitStatus"], inplace=True)

#         # Discount vs Profit
#         plt.figure(figsize=(10, 5))
#         sns.boxplot(x="Discount", y="Profit", data=self.df)
#         plt.title("Profit Distribution by Discount Level")
#         plt.show()

#         # Quantity vs Profit
#         plt.figure(figsize=(8, 4))
#         sns.boxplot(x="Quantity", y="Profit", data=self.df)
#         plt.title("Quantity vs Profit")
#         plt.show()

#     # ==========================
#     # CORRELATION ANALYSIS
#     # ==========================
#     def plot_correlation_matrix(self):
#         cols = ["Quantity", "Discount", "SalesAmount", "Profit"]
#         plt.figure(figsize=(8, 6))
#         sns.heatmap(
#             self.df[cols].corr(),
#             annot=True,
#             cmap="coolwarm"
#         )
#         plt.title("Correlation Matrix")
#         plt.show()
