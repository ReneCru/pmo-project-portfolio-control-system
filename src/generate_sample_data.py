from pathlib import Path
from datetime import datetime, timedelta
import random

import numpy as np
import pandas as pd
from faker import Faker


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

SEED = 42
PROJECT_COUNT = 80
TODAY = datetime(2026, 7, 7)

random.seed(SEED)
np.random.seed(SEED)
Faker.seed(SEED)

fake = Faker()

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Reference Data
# ------------------------------------------------------------

DEPARTMENTS = [
    "Supply Chain",
    "Operations",
    "Quality",
    "Engineering",
    "Finance",
    "IT",
    "Compliance",
    "Procurement",
    "Manufacturing",
    "Customer Service",
]

PROJECT_TYPES = [
    "Process Improvement",
    "Digital Transformation",
    "Cost Reduction",
    "Compliance Initiative",
    "System Implementation",
    "Supplier Development",
    "Operational Excellence",
    "Automation",
    "Data Governance",
    "Customer Experience",
]

PRIORITIES = ["Critical", "High", "Medium", "Low"]

STRATEGIC_ALIGNMENT = ["High", "Medium", "Low"]

BUSINESS_IMPACT = ["High", "Medium", "Low"]

MILESTONE_NAMES = [
    "Project Charter Approved",
    "Requirements Completed",
    "Process Design Completed",
    "Data Validation Completed",
    "System Configuration Completed",
    "User Testing Completed",
    "Training Completed",
    "Go-Live Completed",
    "Post-Go-Live Review Completed",
]

RISK_CATEGORIES = [
    "Schedule",
    "Budget",
    "Resource",
    "Scope",
    "Quality",
    "Compliance",
    "Stakeholder",
    "Technology",
    "Supplier",
    "Operational",
]

RISK_STATUSES = [
    "Open",
    "Mitigation In Progress",
    "Escalated",
    "Closed",
    "Accepted",
]

RISK_DESCRIPTIONS = [
    "Key stakeholder decisions may be delayed.",
    "Project scope may expand beyond the original baseline.",
    "Required resources may not be available on time.",
    "Supplier response time may affect delivery dates.",
    "Budget consumption may exceed the approved plan.",
    "Data quality issues may delay reporting readiness.",
    "System integration complexity may increase implementation effort.",
    "Process owners may not complete validation on schedule.",
    "Compliance requirements may require additional documentation.",
    "Operational workload may limit project execution capacity.",
]


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def classify_risk_level(risk_score: int) -> str:
    """Classify risk level based on probability x impact score."""
    if risk_score <= 5:
        return "Low"
    if risk_score <= 14:
        return "Medium"
    return "High"


def calculate_project_status(start_date: datetime, planned_end_date: datetime) -> str:
    """Assign a realistic project status based on project dates."""
    if start_date > TODAY:
        return "Not Started"

    if planned_end_date < TODAY:
        return random.choices(
            ["Completed", "Active", "On Hold", "Cancelled"],
            weights=[0.55, 0.25, 0.15, 0.05],
            k=1,
        )[0]

    return random.choices(
        ["Active", "On Hold", "Completed", "Cancelled"],
        weights=[0.70, 0.15, 0.10, 0.05],
        k=1,
    )[0]


def calculate_completion_percentage(
    status: str,
    start_date: datetime,
    planned_end_date: datetime,
) -> int:
    """Calculate realistic project completion percentage."""
    if status == "Completed":
        return 100

    if status == "Not Started":
        return 0

    if status == "Cancelled":
        return random.randint(5, 75)

    total_days = max((planned_end_date - start_date).days, 1)
    elapsed_days = max((TODAY - start_date).days, 0)
    baseline_progress = min(elapsed_days / total_days, 1)

    noise = np.random.normal(0, 0.12)
    completion = int((baseline_progress + noise) * 100)

    if status == "On Hold":
        completion = min(completion, random.randint(20, 70))

    return max(5, min(completion, 95))


def calculate_actual_end_date(
    status: str,
    start_date: datetime,
    planned_end_date: datetime,
) -> datetime | None:
    """Generate actual end date only for completed projects, avoiding future dates."""
    if status != "Completed":
        return None

    earliest_possible_end = start_date
    latest_possible_end = min(planned_end_date + timedelta(days=45), TODAY)

    if latest_possible_end < earliest_possible_end:
        return TODAY

    date_range_days = max((latest_possible_end - earliest_possible_end).days, 0)
    return earliest_possible_end + timedelta(days=random.randint(0, date_range_days))


def calculate_schedule_health(status: str, planned_end_date: datetime) -> str:
    """Classify project schedule health."""
    if status == "Completed":
        return "Completed"

    if status == "Cancelled":
        return "Cancelled"

    if status == "Not Started":
        return "Not Started"

    if planned_end_date < TODAY:
        return "Delayed"

    days_to_due = (planned_end_date - TODAY).days

    if days_to_due <= 30:
        return "At Risk"

    return "On Track"


def calculate_budget_values(
    budget: float,
    status: str,
    completion_percentage: int,
) -> tuple:
    """Generate actual cost and forecast cost values."""
    if status == "Completed":
        cost_ratio = np.random.uniform(0.85, 1.25)
    elif status == "Cancelled":
        cost_ratio = np.random.uniform(0.10, 0.75)
    elif status == "Not Started":
        cost_ratio = np.random.uniform(0.00, 0.05)
    else:
        progress_factor = completion_percentage / 100
        cost_ratio = progress_factor + np.random.uniform(-0.10, 0.30)

    cost_ratio = max(cost_ratio, 0)
    actual_cost = round(budget * cost_ratio, 2)

    if status in ["Completed", "Cancelled"]:
        forecast_cost = actual_cost
    else:
        forecast_multiplier = np.random.uniform(0.90, 1.25)
        forecast_cost = round(max(actual_cost, budget * forecast_multiplier), 2)

    return actual_cost, forecast_cost


def generate_project_name(project_type: str, department: str) -> str:
    """Generate a business-style project name."""
    project_keywords = {
        "Process Improvement": [
            "Workflow Optimization",
            "Cycle Time Reduction",
            "Process Standardization",
        ],
        "Digital Transformation": [
            "Digital Control Tower",
            "Reporting Automation",
            "Data Visibility Platform",
        ],
        "Cost Reduction": [
            "Spend Reduction Initiative",
            "Cost Avoidance Program",
            "Efficiency Savings Project",
        ],
        "Compliance Initiative": [
            "Audit Readiness Program",
            "Compliance Documentation Upgrade",
            "Control Review Initiative",
        ],
        "System Implementation": [
            "ERP Enhancement",
            "Business System Rollout",
            "Platform Implementation",
        ],
        "Supplier Development": [
            "Supplier Performance Program",
            "Vendor Risk Reduction",
            "Supplier Scorecard Rollout",
        ],
        "Operational Excellence": [
            "Operational Excellence Program",
            "Lean Execution Initiative",
            "Performance Management Upgrade",
        ],
        "Automation": [
            "Manual Reporting Automation",
            "Workflow Automation",
            "Approval Automation",
        ],
        "Data Governance": [
            "Master Data Quality Program",
            "Data Governance Framework",
            "Data Accuracy Initiative",
        ],
        "Customer Experience": [
            "Customer Response Improvement",
            "Service Performance Initiative",
            "Customer Visibility Upgrade",
        ],
    }

    keyword = random.choice(project_keywords[project_type])
    return f"{department} {keyword}"


def calculate_risk_count(project_status: str, priority: str) -> int:
    """Assign number of risks based on project status and priority."""
    if project_status == "Not Started":
        base_risks = random.randint(0, 2)
    elif project_status == "Completed":
        base_risks = random.randint(0, 2)
    elif project_status == "Cancelled":
        base_risks = random.randint(1, 3)
    elif project_status == "On Hold":
        base_risks = random.randint(2, 4)
    else:
        base_risks = random.randint(1, 4)

    if priority in ["Critical", "High"] and project_status not in ["Completed", "Not Started"]:
        base_risks += random.choice([0, 1])

    return min(base_risks, 5)


def assign_risk_status(project_status: str, risk_level: str) -> str:
    """Assign risk status based on project status and risk level."""
    if project_status == "Completed":
        return random.choices(
            ["Closed", "Accepted", "Open"],
            weights=[0.70, 0.20, 0.10],
            k=1,
        )[0]

    if project_status == "Cancelled":
        return random.choices(
            ["Closed", "Accepted", "Escalated"],
            weights=[0.50, 0.30, 0.20],
            k=1,
        )[0]

    if project_status == "Not Started":
        return random.choices(
            ["Open", "Accepted", "Mitigation In Progress"],
            weights=[0.50, 0.30, 0.20],
            k=1,
        )[0]

    if risk_level == "High":
        return random.choices(
            ["Open", "Mitigation In Progress", "Escalated", "Accepted"],
            weights=[0.25, 0.35, 0.30, 0.10],
            k=1,
        )[0]

    return random.choices(
        RISK_STATUSES,
        weights=[0.30, 0.30, 0.10, 0.20, 0.10],
        k=1,
    )[0]


# ------------------------------------------------------------
# Generate Project Master Data
# ------------------------------------------------------------

project_records = []

project_managers = [fake.name() for _ in range(15)]
sponsors = [fake.name() for _ in range(12)]

for index in range(1, PROJECT_COUNT + 1):
    project_id = f"PMO-{index:04d}"
    department = random.choice(DEPARTMENTS)
    project_type = random.choice(PROJECT_TYPES)
    project_name = generate_project_name(project_type, department)

    start_offset_days = random.randint(-520, 120)
    duration_days = random.randint(75, 420)

    start_date = TODAY + timedelta(days=start_offset_days)
    planned_end_date = start_date + timedelta(days=duration_days)

    status = calculate_project_status(start_date, planned_end_date)
    completion_percentage = calculate_completion_percentage(
        status,
        start_date,
        planned_end_date,
    )

    actual_end_date = calculate_actual_end_date(
        status,
        start_date,
        planned_end_date,
    )

    budget = round(random.randint(50000, 1250000) / 5000) * 5000
    actual_cost, forecast_cost = calculate_budget_values(
        budget,
        status,
        completion_percentage,
    )

    schedule_health = calculate_schedule_health(status, planned_end_date)

    priority = random.choices(
        PRIORITIES,
        weights=[0.15, 0.35, 0.35, 0.15],
        k=1,
    )[0]

    project_records.append(
        {
            "project_id": project_id,
            "project_name": project_name,
            "project_type": project_type,
            "department": department,
            "sponsor": random.choice(sponsors),
            "project_manager": random.choice(project_managers),
            "priority": priority,
            "strategic_alignment": random.choices(
                STRATEGIC_ALIGNMENT,
                weights=[0.45, 0.40, 0.15],
                k=1,
            )[0],
            "business_impact": random.choices(
                BUSINESS_IMPACT,
                weights=[0.40, 0.40, 0.20],
                k=1,
            )[0],
            "status": status,
            "schedule_health": schedule_health,
            "start_date": start_date.date(),
            "planned_end_date": planned_end_date.date(),
            "actual_end_date": actual_end_date.date() if actual_end_date else None,
            "completion_percentage": completion_percentage,
            "budget": budget,
            "actual_cost": actual_cost,
            "forecast_cost": forecast_cost,
        }
    )

project_master_df = pd.DataFrame(project_records)


# ------------------------------------------------------------
# Generate Milestone Tracker Data
# ------------------------------------------------------------

milestone_records = []

for _, project in project_master_df.iterrows():
    milestone_count = random.randint(4, 7)

    start_date = pd.to_datetime(project["start_date"])
    planned_end_date = pd.to_datetime(project["planned_end_date"])
    project_duration_days = max((planned_end_date - start_date).days, 1)

    selected_milestones = random.sample(MILESTONE_NAMES, milestone_count)
    selected_milestones.sort(key=lambda name: MILESTONE_NAMES.index(name))

    for milestone_index, milestone_name in enumerate(selected_milestones, start=1):
        milestone_id = f"MS-{project['project_id']}-{milestone_index:02d}"

        planned_offset = int(project_duration_days * milestone_index / (milestone_count + 1))
        planned_date = start_date + timedelta(days=planned_offset)

        actual_date = None

        if project["status"] == "Completed":
            milestone_status = "Completed"
            actual_date = planned_date + timedelta(days=random.randint(-10, 25))

            if actual_date > TODAY:
                actual_date = TODAY

        elif project["status"] == "Cancelled":
            milestone_status = random.choices(
                ["Completed", "Cancelled", "In Progress"],
                weights=[0.45, 0.45, 0.10],
                k=1,
            )[0]

            if milestone_status == "Completed":
                actual_date = planned_date + timedelta(days=random.randint(-10, 20))
                if actual_date > TODAY:
                    actual_date = TODAY

        elif project["status"] == "Not Started":
            milestone_status = "Not Started"

        else:
            if planned_date < TODAY:
                milestone_status = random.choices(
                    ["Completed", "Delayed", "In Progress"],
                    weights=[0.60, 0.30, 0.10],
                    k=1,
                )[0]

                if milestone_status == "Completed":
                    actual_date = planned_date + timedelta(days=random.randint(-10, 35))
                    if actual_date > TODAY:
                        actual_date = TODAY
            else:
                milestone_status = random.choices(
                    ["Not Started", "In Progress"],
                    weights=[0.75, 0.25],
                    k=1,
                )[0]

        if actual_date:
            delay_days = max((actual_date - planned_date).days, 0)
        elif planned_date < TODAY and milestone_status != "Completed":
            delay_days = max((TODAY - planned_date).days, 0)
        else:
            delay_days = 0

        milestone_records.append(
            {
                "milestone_id": milestone_id,
                "project_id": project["project_id"],
                "milestone_name": milestone_name,
                "owner": project["project_manager"],
                "planned_date": planned_date.date(),
                "actual_date": actual_date.date() if actual_date else None,
                "status": milestone_status,
                "delay_days": delay_days,
            }
        )

milestone_tracker_df = pd.DataFrame(milestone_records)


# ------------------------------------------------------------
# Generate Risk and Issue Log Data
# ------------------------------------------------------------

risk_records = []

for _, project in project_master_df.iterrows():
    risk_count = calculate_risk_count(project["status"], project["priority"])

    for risk_index in range(1, risk_count + 1):
        risk_id = f"RISK-{project['project_id']}-{risk_index:02d}"

        probability = random.randint(1, 5)
        impact = random.randint(1, 5)
        risk_score = probability * impact
        risk_level = classify_risk_level(risk_score)

        status = assign_risk_status(project["status"], risk_level)

        date_identified = pd.to_datetime(project["start_date"]) + timedelta(
            days=random.randint(0, 90)
        )

        if date_identified > TODAY:
            date_identified = TODAY

        mitigation_plan = random.choice(
            [
                "Assign dedicated owner and review weekly.",
                "Create corrective action plan with target completion date.",
                "Escalate blocker during PMO review meeting.",
                "Validate assumptions with process owners.",
                "Increase reporting cadence until risk is reduced.",
                "Review budget and timeline impact with sponsor.",
                "Coordinate mitigation with cross-functional stakeholders.",
            ]
        )

        risk_records.append(
            {
                "risk_id": risk_id,
                "project_id": project["project_id"],
                "risk_category": random.choice(RISK_CATEGORIES),
                "risk_description": random.choice(RISK_DESCRIPTIONS),
                "probability": probability,
                "impact": impact,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_owner": project["project_manager"],
                "mitigation_plan": mitigation_plan,
                "status": status,
                "date_identified": date_identified.date(),
            }
        )

risk_issue_log_df = pd.DataFrame(risk_records)


# ------------------------------------------------------------
# Generate Budget Control Data
# ------------------------------------------------------------

budget_control_df = project_master_df[
    [
        "project_id",
        "project_name",
        "department",
        "project_manager",
        "budget",
        "actual_cost",
        "forecast_cost",
    ]
].copy()

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
# Export CSV Files
# ------------------------------------------------------------

project_master_df.to_csv(RAW_DATA_DIR / "project_master.csv", index=False)
milestone_tracker_df.to_csv(RAW_DATA_DIR / "milestone_tracker.csv", index=False)
risk_issue_log_df.to_csv(RAW_DATA_DIR / "risk_issue_log.csv", index=False)
budget_control_df.to_csv(RAW_DATA_DIR / "budget_control.csv", index=False)


# ------------------------------------------------------------
# Console Summary
# ------------------------------------------------------------

print("Synthetic PMO project portfolio datasets created successfully.")
print(f"Output directory: {RAW_DATA_DIR}")
print(f"Projects generated: {len(project_master_df)}")
print(f"Milestones generated: {len(milestone_tracker_df)}")
print(f"Risks generated: {len(risk_issue_log_df)}")
print(f"Budget records generated: {len(budget_control_df)}")

print("\nFiles created:")
print("- data/raw/project_master.csv")
print("- data/raw/milestone_tracker.csv")
print("- data/raw/risk_issue_log.csv")
print("- data/raw/budget_control.csv")
