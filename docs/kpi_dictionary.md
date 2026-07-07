cat > docs/kpi_dictionary.md <<'EOF'
# KPI Dictionary: PMO Project Portfolio Control System

## 1. Purpose

This KPI Dictionary defines the key performance indicators used in the PMO Project Portfolio Control System.

The objective is to standardize how project portfolio performance is measured across project status, schedule performance, budget control, risk exposure, and executive visibility.

Each KPI includes a definition, business purpose, calculation logic, and expected dashboard usage.

---

## 2. KPI Summary Table

| KPI Name | Category | Purpose |
|---|---|---|
| Total Projects | Portfolio Overview | Measures the total number of projects in the portfolio |
| Active Projects | Portfolio Overview | Tracks projects currently in progress |
| Completed Projects | Portfolio Overview | Tracks projects that have been completed |
| Delayed Projects | Schedule Performance | Identifies projects behind schedule |
| Projects On Track | Schedule Performance | Identifies projects progressing as planned |
| Projects Over Budget | Budget Control | Identifies projects exceeding approved budget |
| Total Portfolio Budget | Budget Control | Measures the total planned budget across all projects |
| Total Actual Cost | Budget Control | Measures actual spend across all projects |
| Budget Variance | Budget Control | Compares planned budget against actual cost |
| Cost Overrun Percentage | Budget Control | Measures how much a project exceeded budget |
| Average Completion Percentage | Portfolio Progress | Measures average progress across the portfolio |
| Overdue Milestones | Milestone Control | Tracks milestones not completed by the planned date |
| Average Delay Days | Schedule Performance | Measures average delay across delayed milestones |
| High Risk Projects | Risk Management | Identifies projects with high risk exposure |
| Portfolio Risk Exposure | Risk Management | Measures total risk exposure across the portfolio |
| Projects by Department | Portfolio Segmentation | Shows project distribution by business area |
| Projects by Priority | Portfolio Segmentation | Shows project distribution by priority level |
| Projects by Status | Portfolio Segmentation | Shows project distribution by current status |

---

## 3. Portfolio Overview KPIs

### 3.1 Total Projects

**Definition:**  
Total number of projects included in the portfolio.

**Business Purpose:**  
Provides leadership with a high-level view of the size of the active project portfolio.

**Calculation Logic:**  

```text
Total Projects = Count of Project ID