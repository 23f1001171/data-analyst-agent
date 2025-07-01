import duckdb
import pandas as pd
from typing import Optional

def execute_duckdb_query(query: str) -> pd.DataFrame:
    try:
        conn = duckdb.connect()
        result = conn.execute(query).fetchdf()
        conn.close()
        return result
    except Exception as e:
        raise Exception(f"DuckDB query failed: {str(e)}")