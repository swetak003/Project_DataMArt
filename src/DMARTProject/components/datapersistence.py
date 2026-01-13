from sqlalchemy import create_engine, text
import pandas as pd

class DataPersistence:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)

    def write_to_sql(self, df, table_name, mode="replace"):
        df.to_sql(
        name=table_name,
        con=self.engine,
        if_exists=mode,
        index=False
    )
    def call_stored_procedure(self, sp_name: str):
        with self.engine.begin() as conn:
            conn.execute(text(f"EXEC {sp_name}"))
