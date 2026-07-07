from pathlib import Path
import sqlite3

import pandas as pd


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "data" / "pmo_portfolio.db"
SQL_CREATE_TABLES_PATH = BASE_DIR / "sql" / "create_tables.sql"


# ------------------------------------------------------------
# Table Load Configuration
# ------------------------------------------------------------

TABLE_LOAD_ORDER = [
    {
        "table_name": "project_master",
        "file_name": "project_master_clean.csv",
    },
    {
        "table_name": "milestone_tracker",
        "file_name": "milestone_tracker_clean.csv",
    },
    {
        "table_name": "risk_issue_log",
        "file_name": "risk_issue_log_clean.csv",
    },
    {
        "table_name": "budget_control",
        "file_name": "budget_control_clean.csv",
    },
    {
        "table_name": "project_portfolio_enriched",
        "file_name": "project_portfolio_enriched.csv",
    },
]


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def validate_required_files() -> None:
    """Validate that required SQL and CSV files exist before loading data."""
    if not SQL_CREATE_TABLES_PATH.exists():
        raise FileNotFoundError(
            f"Missing SQL table creation script: {SQL_CREATE_TABLES_PATH}"
        )

    for table_config in TABLE_LOAD_ORDER:
        file_path = PROCESSED_DATA_DIR / table_config["file_name"]

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing processed CSV file: {file_path}. "
                "Run src/clean_portfolio_data.py before this script."
            )


def convert_boolean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert boolean columns to 1/0 for SQLite compatibility."""
    boolean_columns = df.select_dtypes(include=["bool"]).columns

    for column in boolean_columns:
        df[column] = df[column].astype(int)

    return df


def load_csv_to_table(
    connection: sqlite3.Connection,
    table_name: str,
    file_name: str,
) -> int:
    """Load a processed CSV file into a SQLite table."""
    file_path = PROCESSED_DATA_DIR / file_name

    df = pd.read_csv(file_path)
    df = convert_boolean_columns(df)

    df.to_sql(
        table_name,
        connection,
        if_exists="append",
        index=False,
    )

    return len(df)


def count_table_rows(connection: sqlite3.Connection, table_name: str) -> int:
    """Return number of records in a SQLite table."""
    query = f"SELECT COUNT(*) FROM {table_name};"
    result = connection.execute(query).fetchone()
    return result[0]


# ------------------------------------------------------------
# Main Script
# ------------------------------------------------------------

validate_required_files()

connection = sqlite3.connect(DB_PATH)

with open(SQL_CREATE_TABLES_PATH, "r", encoding="utf-8") as sql_file:
    create_tables_script = sql_file.read()

connection.executescript(create_tables_script)

loaded_records = []

for table_config in TABLE_LOAD_ORDER:
    table_name = table_config["table_name"]
    file_name = table_config["file_name"]

    rows_loaded = load_csv_to_table(
        connection=connection,
        table_name=table_name,
        file_name=file_name,
    )

    loaded_records.append(
        {
            "table_name": table_name,
            "source_file": file_name,
            "rows_loaded": rows_loaded,
            "rows_in_database": count_table_rows(connection, table_name),
        }
    )

connection.commit()

loaded_summary_df = pd.DataFrame(loaded_records)

print("PMO portfolio data loaded into SQLite successfully.")
print(f"Database path: {DB_PATH}")

print("\nTables loaded:")
print(loaded_summary_df.to_string(index=False))

print("\nSample validation query:")
sample_query = """
SELECT
    traffic_light_status,
    COUNT(*) AS total_projects,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost
FROM project_portfolio_enriched
GROUP BY traffic_light_status
ORDER BY
    CASE traffic_light_status
        WHEN 'Red' THEN 1
        WHEN 'Yellow' THEN 2
        WHEN 'Green' THEN 3
        ELSE 4
    END;
"""

sample_result_df = pd.read_sql_query(sample_query, connection)
print(sample_result_df.to_string(index=False))

connection.close()
