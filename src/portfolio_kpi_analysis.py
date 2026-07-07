from pathlib import Path

import numpy as np
import pandas as pd


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def load_processed_portfolio() -> pd.DataFrame:
    """Load the enriched project portfolio dataset."""
    file_path = PROCESSED_DATA_DIR / "project_portfolio_enriched.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "Missing project_portfolio_enriched.csv. "
            "Run src/clean_portfolio_data.py before this script."
        )

    return pd.read_csv(file_path)


def calculate_percentage(numerator: float, denominator: float) -> float:
    """Safely calculate percentage."""
    if denominator == 0:
        return 0.0

    return round((numerator / denominator) * 100, 2)


def calculate_overall_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate portfolio-level executive KPIs."""
    total_projects = len(df)

    active_projects = int((df["status"] == "Active").sum())
    completed_projects = int((df["status"] == "Completed").sum())
    delayed_projects = int(df["is_delayed"].sum())
    over_budget_projects = int(df["is_over_budget"].sum())
    forecast_over_budget_projects = int(df["is_forecast_over_budget"].sum())
    projects_requiring_attention = int(df["requires_executive_attention"].sum())

    total_budget = round(df["budget"].sum(), 2)
    total_actual_cost = round(df["actual_cost"].sum(), 2)
    total_forecast_cost = round(df["forecast_cost"].sum(), 2)
    total_budget_variance = round(df["budget_variance"].sum(), 2)
    total_forecast_variance = round(df["forecast_variance"].sum(), 2)

    high_risk_projects = int((df["high_risks"] > 0).sum())
    escalated_risk_projects = int((df["escalated_risks"] > 0).sum())
    total_open_risks = int(df["open_risks"].sum())
    total_high_risks = int(df["high_risks"].sum())
    total_escalated_risks = int(df["escalated_risks"].sum())
    total_portfolio_risk_exposure = int(df["portfolio_risk_exposure"].sum())

    total_overdue_milestones = int(df["overdue_milestones"].sum())
    total_milestones = int(df["total_milestones"].sum())
    completed_milestones = int(df["completed_milestones"].sum())

    average_completion = round(df["completion_percentage"].mean(), 2)
    average_milestone_completion = round(df["milestone_completion_rate"].mean(), 2)

    delayed_df = df[df["is_delayed"] == True]
    average_delay_days = round(delayed_df["project_delay_days"].mean(), 2) if len(delayed_df) > 0 else 0

    kpi_records = [
        {
            "kpi_name": "Total Projects",
            "kpi_value": total_projects,
            "kpi_category": "Portfolio Overview",
        },
        {
            "kpi_name": "Active Projects",
            "kpi_value": active_projects,
            "kpi_category": "Portfolio Overview",
        },
        {
            "kpi_name": "Completed Projects",
            "kpi_value": completed_projects,
            "kpi_category": "Portfolio Overview",
        },
        {
            "kpi_name": "Delayed Projects",
            "kpi_value": delayed_projects,
            "kpi_category": "Schedule Performance",
        },
        {
            "kpi_name": "Projects Over Budget",
            "kpi_value": over_budget_projects,
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Forecast Over Budget Projects",
            "kpi_value": forecast_over_budget_projects,
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Projects Requiring Executive Attention",
            "kpi_value": projects_requiring_attention,
            "kpi_category": "Executive Control",
        },
        {
            "kpi_name": "Total Portfolio Budget",
            "kpi_value": total_budget,
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Total Actual Cost",
            "kpi_value": total_actual_cost,
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Total Forecast Cost",
            "kpi_value": total_forecast_cost,
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Total Budget Variance",
            "kpi_value": total_budget_variance,
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Total Forecast Variance",
            "kpi_value": total_forecast_variance,
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Average Completion Percentage",
            "kpi_value": average_completion,
            "kpi_category": "Portfolio Progress",
        },
        {
            "kpi_name": "High Risk Projects",
            "kpi_value": high_risk_projects,
            "kpi_category": "Risk Management",
        },
        {
            "kpi_name": "Escalated Risk Projects",
            "kpi_value": escalated_risk_projects,
            "kpi_category": "Risk Management",
        },
        {
            "kpi_name": "Total Open Risks",
            "kpi_value": total_open_risks,
            "kpi_category": "Risk Management",
        },
        {
            "kpi_name": "Total High Risks",
            "kpi_value": total_high_risks,
            "kpi_category": "Risk Management",
        },
        {
            "kpi_name": "Total Escalated Risks",
            "kpi_value": total_escalated_risks,
            "kpi_category": "Risk Management",
        },
        {
            "kpi_name": "Portfolio Risk Exposure",
            "kpi_value": total_portfolio_risk_exposure,
            "kpi_category": "Risk Management",
        },
        {
            "kpi_name": "Total Milestones",
            "kpi_value": total_milestones,
            "kpi_category": "Milestone Control",
        },
        {
            "kpi_name": "Completed Milestones",
            "kpi_value": completed_milestones,
            "kpi_category": "Milestone Control",
        },
        {
            "kpi_name": "Overdue Milestones",
            "kpi_value": total_overdue_milestones,
            "kpi_category": "Milestone Control",
        },
        {
            "kpi_name": "Average Milestone Completion Rate",
            "kpi_value": average_milestone_completion,
            "kpi_category": "Milestone Control",
        },
        {
            "kpi_name": "Average Delay Days",
            "kpi_value": average_delay_days,
            "kpi_category": "Schedule Performance",
        },
        {
            "kpi_name": "Portfolio Completion Rate",
            "kpi_value": calculate_percentage(completed_projects, total_projects),
            "kpi_category": "Portfolio Overview",
        },
        {
            "kpi_name": "Delayed Project Rate",
            "kpi_value": calculate_percentage(delayed_projects, total_projects),
            "kpi_category": "Schedule Performance",
        },
        {
            "kpi_name": "Over Budget Project Rate",
            "kpi_value": calculate_percentage(over_budget_projects, total_projects),
            "kpi_category": "Budget Control",
        },
        {
            "kpi_name": "Executive Attention Rate",
            "kpi_value": calculate_percentage(projects_requiring_attention, total_projects),
            "kpi_category": "Executive Control",
        },
    ]

    return pd.DataFrame(kpi_records)


def create_department_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Create department-level performance summary."""
    department_df = (
        df.groupby("department")
        .agg(
            total_projects=("project_id", "count"),
            active_projects=("status", lambda x: (x == "Active").sum()),
            completed_projects=("status", lambda x: (x == "Completed").sum()),
            delayed_projects=("is_delayed", "sum"),
            over_budget_projects=("is_over_budget", "sum"),
            projects_requiring_attention=("requires_executive_attention", "sum"),
            average_completion=("completion_percentage", "mean"),
            total_budget=("budget", "sum"),
            total_actual_cost=("actual_cost", "sum"),
            total_forecast_cost=("forecast_cost", "sum"),
            total_budget_variance=("budget_variance", "sum"),
            total_open_risks=("open_risks", "sum"),
            total_high_risks=("high_risks", "sum"),
            total_escalated_risks=("escalated_risks", "sum"),
            total_overdue_milestones=("overdue_milestones", "sum"),
            total_risk_exposure=("portfolio_risk_exposure", "sum"),
        )
        .reset_index()
    )

    department_df["average_completion"] = department_df["average_completion"].round(2)
    department_df["delayed_project_rate"] = department_df.apply(
        lambda row: calculate_percentage(row["delayed_projects"], row["total_projects"]),
        axis=1,
    )
    department_df["attention_rate"] = department_df.apply(
        lambda row: calculate_percentage(row["projects_requiring_attention"], row["total_projects"]),
        axis=1,
    )
    department_df["budget_utilization_rate"] = department_df.apply(
        lambda row: calculate_percentage(row["total_actual_cost"], row["total_budget"]),
        axis=1,
    )

    department_df = department_df.sort_values(
        by=["projects_requiring_attention", "total_risk_exposure", "total_budget"],
        ascending=[False, False, False],
    )

    return department_df


def create_project_manager_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Create project manager-level performance summary."""
    manager_df = (
        df.groupby("project_manager")
        .agg(
            total_projects=("project_id", "count"),
            active_projects=("status", lambda x: (x == "Active").sum()),
            completed_projects=("status", lambda x: (x == "Completed").sum()),
            delayed_projects=("is_delayed", "sum"),
            over_budget_projects=("is_over_budget", "sum"),
            projects_requiring_attention=("requires_executive_attention", "sum"),
            average_completion=("completion_percentage", "mean"),
            total_budget=("budget", "sum"),
            total_actual_cost=("actual_cost", "sum"),
            total_budget_variance=("budget_variance", "sum"),
            total_open_risks=("open_risks", "sum"),
            total_high_risks=("high_risks", "sum"),
            total_overdue_milestones=("overdue_milestones", "sum"),
            total_risk_exposure=("portfolio_risk_exposure", "sum"),
        )
        .reset_index()
    )

    manager_df["average_completion"] = manager_df["average_completion"].round(2)
    manager_df["attention_rate"] = manager_df.apply(
        lambda row: calculate_percentage(row["projects_requiring_attention"], row["total_projects"]),
        axis=1,
    )
    manager_df["delayed_project_rate"] = manager_df.apply(
        lambda row: calculate_percentage(row["delayed_projects"], row["total_projects"]),
        axis=1,
    )
    manager_df["budget_utilization_rate"] = manager_df.apply(
        lambda row: calculate_percentage(row["total_actual_cost"], row["total_budget"]),
        axis=1,
    )

    manager_df = manager_df.sort_values(
        by=["projects_requiring_attention", "total_risk_exposure", "total_projects"],
        ascending=[False, False, False],
    )

    return manager_df


def create_traffic_light_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create traffic light distribution summary."""
    traffic_df = (
        df.groupby("traffic_light_status")
        .agg(
            total_projects=("project_id", "count"),
            total_budget=("budget", "sum"),
            total_actual_cost=("actual_cost", "sum"),
            total_open_risks=("open_risks", "sum"),
            total_high_risks=("high_risks", "sum"),
            total_overdue_milestones=("overdue_milestones", "sum"),
            average_completion=("completion_percentage", "mean"),
        )
        .reset_index()
    )

    total_projects = len(df)
    traffic_df["portfolio_percentage"] = traffic_df["total_projects"].apply(
        lambda value: calculate_percentage(value, total_projects)
    )

    traffic_order = {"Red": 1, "Yellow": 2, "Green": 3}
    traffic_df["sort_order"] = traffic_df["traffic_light_status"].map(traffic_order)
    traffic_df = traffic_df.sort_values("sort_order").drop(columns=["sort_order"])

    traffic_df["average_completion"] = traffic_df["average_completion"].round(2)

    return traffic_df


def create_budget_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Create budget performance analysis by budget category."""
    budget_df = (
        df.groupby("budget_variance_category")
        .agg(
            total_projects=("project_id", "count"),
            total_budget=("budget", "sum"),
            total_actual_cost=("actual_cost", "sum"),
            total_forecast_cost=("forecast_cost", "sum"),
            total_budget_variance=("budget_variance", "sum"),
            total_forecast_variance=("forecast_variance", "sum"),
            average_cost_overrun_percentage=("cost_overrun_percentage", "mean"),
            projects_requiring_attention=("requires_executive_attention", "sum"),
        )
        .reset_index()
    )

    budget_df["average_cost_overrun_percentage"] = (
        budget_df["average_cost_overrun_percentage"].round(2)
    )

    budget_df = budget_df.sort_values(
        by=["projects_requiring_attention", "total_actual_cost"],
        ascending=[False, False],
    )

    return budget_df


def create_risk_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Create risk exposure analysis by risk exposure flag."""
    risk_df = (
        df.groupby("risk_exposure_flag")
        .agg(
            total_projects=("project_id", "count"),
            total_open_risks=("open_risks", "sum"),
            total_high_risks=("high_risks", "sum"),
            total_escalated_risks=("escalated_risks", "sum"),
            total_risk_exposure=("portfolio_risk_exposure", "sum"),
            average_max_risk_score=("max_risk_score", "mean"),
            projects_requiring_attention=("requires_executive_attention", "sum"),
            total_overdue_milestones=("overdue_milestones", "sum"),
            total_budget=("budget", "sum"),
        )
        .reset_index()
    )

    risk_df["average_max_risk_score"] = risk_df["average_max_risk_score"].round(2)

    risk_order = {"High": 1, "Medium": 2, "Low": 3}
    risk_df["sort_order"] = risk_df["risk_exposure_flag"].map(risk_order)
    risk_df = risk_df.sort_values("sort_order").drop(columns=["sort_order"])

    return risk_df


def create_top_projects_requiring_attention(df: pd.DataFrame) -> pd.DataFrame:
    """Create ranked list of projects requiring executive attention."""
    attention_df = df[df["requires_executive_attention"] == True].copy()

    attention_df["attention_score"] = (
        attention_df["high_risks"] * 5
        + attention_df["escalated_risks"] * 5
        + attention_df["overdue_milestones"] * 3
        + attention_df["is_over_budget"].astype(int) * 4
        + attention_df["is_delayed"].astype(int) * 4
        + attention_df["cost_overrun_percentage"]
    )

    selected_columns = [
        "project_id",
        "project_name",
        "department",
        "project_manager",
        "priority",
        "status",
        "traffic_light_status",
        "schedule_health",
        "completion_percentage",
        "budget",
        "actual_cost",
        "budget_variance",
        "cost_overrun_percentage",
        "project_delay_days",
        "overdue_milestones",
        "high_risks",
        "escalated_risks",
        "portfolio_risk_exposure",
        "attention_score",
    ]

    attention_df = attention_df[selected_columns].sort_values(
        by="attention_score",
        ascending=False,
    )

    return attention_df


# ------------------------------------------------------------
# Main Script
# ------------------------------------------------------------

portfolio_df = load_processed_portfolio()

overall_kpis_df = calculate_overall_kpis(portfolio_df)
department_performance_df = create_department_performance(portfolio_df)
project_manager_performance_df = create_project_manager_performance(portfolio_df)
traffic_light_summary_df = create_traffic_light_summary(portfolio_df)
budget_analysis_df = create_budget_analysis(portfolio_df)
risk_analysis_df = create_risk_analysis(portfolio_df)
top_attention_projects_df = create_top_projects_requiring_attention(portfolio_df)


# ------------------------------------------------------------
# Export KPI Outputs
# ------------------------------------------------------------

overall_kpis_df.to_csv(
    OUTPUTS_DIR / "portfolio_kpi_summary.csv",
    index=False,
)

department_performance_df.to_csv(
    OUTPUTS_DIR / "department_performance_summary.csv",
    index=False,
)

project_manager_performance_df.to_csv(
    OUTPUTS_DIR / "project_manager_performance_summary.csv",
    index=False,
)

traffic_light_summary_df.to_csv(
    OUTPUTS_DIR / "traffic_light_summary.csv",
    index=False,
)

budget_analysis_df.to_csv(
    OUTPUTS_DIR / "budget_analysis_summary.csv",
    index=False,
)

risk_analysis_df.to_csv(
    OUTPUTS_DIR / "risk_analysis_summary.csv",
    index=False,
)

top_attention_projects_df.to_csv(
    OUTPUTS_DIR / "top_projects_requiring_attention.csv",
    index=False,
)


# ------------------------------------------------------------
# Console Summary
# ------------------------------------------------------------

print("PMO portfolio KPI analysis completed successfully.")

print("\nFiles created:")
print("- outputs/portfolio_kpi_summary.csv")
print("- outputs/department_performance_summary.csv")
print("- outputs/project_manager_performance_summary.csv")
print("- outputs/traffic_light_summary.csv")
print("- outputs/budget_analysis_summary.csv")
print("- outputs/risk_analysis_summary.csv")
print("- outputs/top_projects_requiring_attention.csv")

print("\nPortfolio KPI Summary:")
print(overall_kpis_df.to_string(index=False))

print("\nTraffic Light Summary:")
print(traffic_light_summary_df.to_string(index=False))

print("\nTop 10 Projects Requiring Attention:")
print(top_attention_projects_df.head(10).to_string(index=False))
