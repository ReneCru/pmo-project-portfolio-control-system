from pathlib import Path

import numpy as np
import pandas as pd


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

TODAY = pd.Timestamp("2026-07-07")

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def load_csv(file_name: str) -> pd.DataFrame:
    """Load a CSV file from the raw data directory."""
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Missing required file: {file_path}")

    return pd.read_csv(file_path)


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading and trailing spaces from text columns."""
    text_columns = df.select_dtypes(include=["object", "str", "string"]).columns

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()
        df[column] = df[column].replace({"nan": np.nan, "None": np.nan})

    return df


def parse_date_columns(df: pd.DataFrame, date_columns: list[str]) -> pd.DataFrame:
    """Convert selected columns to datetime format."""
    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def classify_budget_variance(row: pd.Series) -> str:
    """Classify project budget performance."""
    if row["actual_cost"] > row["budget"]:
        return "Over Budget"

    if row["forecast_cost"] > row["budget"]:
        return "Forecast Over Budget"

    if row["budget_variance"] >= row["budget"] * 0.10:
        return "Under Budget >10%"

    return "Within Budget"


def classify_risk_exposure(row: pd.Series) -> str:
    """Classify project risk exposure level."""
    if (
        row["high_risks"] > 0
        or row["escalated_risks"] > 0
        or row["portfolio_risk_exposure"] >= 30
        or row["max_risk_score"] >= 15
    ):
        return "High"

    if row["open_risks"] > 0 or row["portfolio_risk_exposure"] >= 10:
        return "Medium"

    return "Low"


def classify_traffic_light(row: pd.Series) -> str:
    """Assign executive traffic light status."""
    if (
        row["status"] == "Cancelled"
        or row["is_delayed"]
        or row["is_over_budget"]
        or row["high_risks"] > 0
        or row["escalated_risks"] > 0
        or row["overdue_milestones"] >= 2
    ):
        return "Red"

    if (
        row["schedule_health"] == "At Risk"
        or row["is_forecast_over_budget"]
        or row["overdue_milestones"] == 1
        or row["open_risks"] > 0
    ):
        return "Yellow"

    return "Green"


# ------------------------------------------------------------
# Load Raw Datasets
# ------------------------------------------------------------

project_master_df = load_csv("project_master.csv")
milestone_tracker_df = load_csv("milestone_tracker.csv")
risk_issue_log_df = load_csv("risk_issue_log.csv")
budget_control_df = load_csv("budget_control.csv")


# ------------------------------------------------------------
# Clean Project Master Data
# ------------------------------------------------------------

project_master_df = clean_text_columns(project_master_df)

project_master_df = parse_date_columns(
    project_master_df,
    ["start_date", "planned_end_date", "actual_end_date"],
)

numeric_project_columns = [
    "completion_percentage",
    "budget",
    "actual_cost",
    "forecast_cost",
]

for column in numeric_project_columns:
    project_master_df[column] = pd.to_numeric(
        project_master_df[column],
        errors="coerce",
    ).fillna(0)

project_master_df["budget_variance"] = (
    project_master_df["budget"] - project_master_df["actual_cost"]
).round(2)

project_master_df["forecast_variance"] = (
    project_master_df["budget"] - project_master_df["forecast_cost"]
).round(2)

project_master_df["is_completed"] = project_master_df["status"] == "Completed"

project_master_df["is_delayed"] = (
    (project_master_df["planned_end_date"] < TODAY)
    & (~project_master_df["status"].isin(["Completed", "Cancelled", "Not Started"]))
)

project_master_df["is_over_budget"] = (
    project_master_df["actual_cost"] > project_master_df["budget"]
)

project_master_df["is_forecast_over_budget"] = (
    project_master_df["forecast_cost"] > project_master_df["budget"]
)

project_master_df["days_until_due"] = (
    project_master_df["planned_end_date"] - TODAY
).dt.days

project_master_df["project_delay_days"] = np.where(
    project_master_df["is_delayed"],
    (TODAY - project_master_df["planned_end_date"]).dt.days,
    0,
)


# ------------------------------------------------------------
# Clean Milestone Tracker Data
# ------------------------------------------------------------

milestone_tracker_df = clean_text_columns(milestone_tracker_df)

milestone_tracker_df = parse_date_columns(
    milestone_tracker_df,
    ["planned_date", "actual_date"],
)

milestone_tracker_df["delay_days"] = pd.to_numeric(
    milestone_tracker_df["delay_days"],
    errors="coerce",
).fillna(0)

milestone_tracker_df["is_completed_milestone"] = (
    milestone_tracker_df["status"] == "Completed"
)

milestone_tracker_df["is_overdue_milestone"] = (
    (milestone_tracker_df["planned_date"] < TODAY)
    & (milestone_tracker_df["status"] != "Completed")
)

milestone_tracker_df["overdue_delay_days"] = np.where(
    milestone_tracker_df["is_overdue_milestone"],
    milestone_tracker_df["delay_days"],
    0,
)


# ------------------------------------------------------------
# Clean Risk and Issue Log Data
# ------------------------------------------------------------

risk_issue_log_df = clean_text_columns(risk_issue_log_df)

risk_issue_log_df = parse_date_columns(
    risk_issue_log_df,
    ["date_identified"],
)

numeric_risk_columns = ["probability", "impact", "risk_score"]

for column in numeric_risk_columns:
    risk_issue_log_df[column] = pd.to_numeric(
        risk_issue_log_df[column],
        errors="coerce",
    ).fillna(0)

risk_issue_log_df["is_open_risk"] = risk_issue_log_df["status"] != "Closed"
risk_issue_log_df["is_high_risk"] = risk_issue_log_df["risk_level"] == "High"
risk_issue_log_df["is_escalated"] = risk_issue_log_df["status"] == "Escalated"

risk_issue_log_df["open_risk_score"] = np.where(
    risk_issue_log_df["is_open_risk"],
    risk_issue_log_df["risk_score"],
    0,
)


# ------------------------------------------------------------
# Clean Budget Control Data
# ------------------------------------------------------------

budget_control_df = clean_text_columns(budget_control_df)

numeric_budget_columns = [
    "budget",
    "actual_cost",
    "forecast_cost",
    "budget_variance",
    "forecast_variance",
    "cost_overrun_percentage",
]

for column in numeric_budget_columns:
    budget_control_df[column] = pd.to_numeric(
        budget_control_df[column],
        errors="coerce",
    ).fillna(0)

budget_control_df["budget_variance"] = (
    budget_control_df["budget"] - budget_control_df["actual_cost"]
).round(2)

budget_control_df["forecast_variance"] = (
    budget_control_df["budget"] - budget_control_df["forecast_cost"]
).round(2)

budget_control_df["cost_overrun_percentage"] = np.where(
    budget_control_df["actual_cost"] > budget_control_df["budget"],
    (
        (budget_control_df["actual_cost"] - budget_control_df["budget"])
        / budget_control_df["budget"]
        * 100
    ).round(2),
    0,
)

budget_control_df["budget_status"] = np.where(
    budget_control_df["actual_cost"] > budget_control_df["budget"],
    "Over Budget",
    "Within Budget",
)


# ------------------------------------------------------------
# Create Milestone Summary by Project
# ------------------------------------------------------------

milestone_summary_df = (
    milestone_tracker_df
    .groupby("project_id")
    .agg(
        total_milestones=("milestone_id", "count"),
        completed_milestones=("is_completed_milestone", "sum"),
        overdue_milestones=("is_overdue_milestone", "sum"),
        total_milestone_delay_days=("delay_days", "sum"),
        total_overdue_delay_days=("overdue_delay_days", "sum"),
    )
    .reset_index()
)

milestone_summary_df["milestone_completion_rate"] = np.where(
    milestone_summary_df["total_milestones"] > 0,
    (
        milestone_summary_df["completed_milestones"]
        / milestone_summary_df["total_milestones"]
        * 100
    ).round(2),
    0,
)


# ------------------------------------------------------------
# Create Risk Summary by Project
# ------------------------------------------------------------

risk_summary_df = (
    risk_issue_log_df
    .groupby("project_id")
    .agg(
        total_risks=("risk_id", "count"),
        open_risks=("is_open_risk", "sum"),
        high_risks=("is_high_risk", "sum"),
        escalated_risks=("is_escalated", "sum"),
        portfolio_risk_exposure=("open_risk_score", "sum"),
        max_risk_score=("risk_score", "max"),
    )
    .reset_index()
)


# ------------------------------------------------------------
# Create Enriched Project Portfolio Dataset
# ------------------------------------------------------------

project_portfolio_enriched_df = project_master_df.merge(
    milestone_summary_df,
    on="project_id",
    how="left",
)

project_portfolio_enriched_df = project_portfolio_enriched_df.merge(
    risk_summary_df,
    on="project_id",
    how="left",
)

budget_fields = [
    "project_id",
    "budget_variance",
    "forecast_variance",
    "cost_overrun_percentage",
    "budget_status",
]

project_portfolio_enriched_df = project_portfolio_enriched_df.drop(
    columns=["budget_variance", "forecast_variance"],
    errors="ignore",
)

project_portfolio_enriched_df = project_portfolio_enriched_df.merge(
    budget_control_df[budget_fields],
    on="project_id",
    how="left",
)

summary_columns_to_fill = [
    "total_milestones",
    "completed_milestones",
    "overdue_milestones",
    "total_milestone_delay_days",
    "total_overdue_delay_days",
    "milestone_completion_rate",
    "total_risks",
    "open_risks",
    "high_risks",
    "escalated_risks",
    "portfolio_risk_exposure",
    "max_risk_score",
    "cost_overrun_percentage",
]

for column in summary_columns_to_fill:
    project_portfolio_enriched_df[column] = (
        project_portfolio_enriched_df[column]
        .fillna(0)
        .astype(float)
    )

integer_columns = [
    "total_milestones",
    "completed_milestones",
    "overdue_milestones",
    "total_milestone_delay_days",
    "total_overdue_delay_days",
    "total_risks",
    "open_risks",
    "high_risks",
    "escalated_risks",
    "portfolio_risk_exposure",
    "max_risk_score",
]

for column in integer_columns:
    project_portfolio_enriched_df[column] = (
        project_portfolio_enriched_df[column]
        .round(0)
        .astype(int)
    )

project_portfolio_enriched_df["budget_variance_category"] = (
    project_portfolio_enriched_df.apply(classify_budget_variance, axis=1)
)

project_portfolio_enriched_df["risk_exposure_flag"] = (
    project_portfolio_enriched_df.apply(classify_risk_exposure, axis=1)
)

project_portfolio_enriched_df["traffic_light_status"] = (
    project_portfolio_enriched_df.apply(classify_traffic_light, axis=1)
)

project_portfolio_enriched_df["requires_executive_attention"] = (
    project_portfolio_enriched_df["traffic_light_status"] == "Red"
)


# ------------------------------------------------------------
# Create Executive Summary Output
# ------------------------------------------------------------

executive_summary_df = pd.DataFrame(
    [
        {
            "generated_on": TODAY.date(),
            "total_projects": len(project_portfolio_enriched_df),
            "active_projects": int((project_portfolio_enriched_df["status"] == "Active").sum()),
            "completed_projects": int((project_portfolio_enriched_df["status"] == "Completed").sum()),
            "delayed_projects": int(project_portfolio_enriched_df["is_delayed"].sum()),
            "projects_over_budget": int(project_portfolio_enriched_df["is_over_budget"].sum()),
            "forecast_over_budget_projects": int(project_portfolio_enriched_df["is_forecast_over_budget"].sum()),
            "projects_requiring_attention": int(project_portfolio_enriched_df["requires_executive_attention"].sum()),
            "high_risk_projects": int((project_portfolio_enriched_df["high_risks"] > 0).sum()),
            "total_open_risks": int(project_portfolio_enriched_df["open_risks"].sum()),
            "total_overdue_milestones": int(project_portfolio_enriched_df["overdue_milestones"].sum()),
            "total_portfolio_budget": round(project_portfolio_enriched_df["budget"].sum(), 2),
            "total_actual_cost": round(project_portfolio_enriched_df["actual_cost"].sum(), 2),
            "total_forecast_cost": round(project_portfolio_enriched_df["forecast_cost"].sum(), 2),
            "total_budget_variance": round(project_portfolio_enriched_df["budget_variance"].sum(), 2),
            "average_completion_percentage": round(project_portfolio_enriched_df["completion_percentage"].mean(), 2),
        }
    ]
)

projects_requiring_attention_df = project_portfolio_enriched_df[
    project_portfolio_enriched_df["requires_executive_attention"]
].copy()

projects_requiring_attention_df = projects_requiring_attention_df.sort_values(
    by=[
        "high_risks",
        "escalated_risks",
        "overdue_milestones",
        "cost_overrun_percentage",
        "project_delay_days",
    ],
    ascending=[False, False, False, False, False],
)


# ------------------------------------------------------------
# Export Processed Files
# ------------------------------------------------------------

project_master_df.to_csv(
    PROCESSED_DATA_DIR / "project_master_clean.csv",
    index=False,
)

milestone_tracker_df.to_csv(
    PROCESSED_DATA_DIR / "milestone_tracker_clean.csv",
    index=False,
)

risk_issue_log_df.to_csv(
    PROCESSED_DATA_DIR / "risk_issue_log_clean.csv",
    index=False,
)

budget_control_df.to_csv(
    PROCESSED_DATA_DIR / "budget_control_clean.csv",
    index=False,
)

project_portfolio_enriched_df.to_csv(
    PROCESSED_DATA_DIR / "project_portfolio_enriched.csv",
    index=False,
)

executive_summary_df.to_csv(
    OUTPUTS_DIR / "executive_summary.csv",
    index=False,
)

projects_requiring_attention_df.to_csv(
    OUTPUTS_DIR / "projects_requiring_attention.csv",
    index=False,
)


# ------------------------------------------------------------
# Console Summary
# ------------------------------------------------------------

print("PMO portfolio data cleaning completed successfully.")
print(f"Processed data directory: {PROCESSED_DATA_DIR}")
print(f"Outputs directory: {OUTPUTS_DIR}")

print("\nProcessed files created:")
print("- data/processed/project_master_clean.csv")
print("- data/processed/milestone_tracker_clean.csv")
print("- data/processed/risk_issue_log_clean.csv")
print("- data/processed/budget_control_clean.csv")
print("- data/processed/project_portfolio_enriched.csv")

print("\nExecutive output files created:")
print("- outputs/executive_summary.csv")
print("- outputs/projects_requiring_attention.csv")

print("\nExecutive summary:")
print(executive_summary_df.to_string(index=False))
