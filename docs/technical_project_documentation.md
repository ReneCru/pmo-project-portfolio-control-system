# Technical Project Documentation: PMO Project Portfolio Control System

## 1. Project Overview

The PMO Project Portfolio Control System is a business analytics project designed to simulate how a Project Management Office can monitor portfolio health, budget performance, milestone execution, risk exposure, and executive attention priorities.

The project combines Python, SQL, SQLite, CSV datasets, business documentation, and Power BI planning documentation.

The goal is to demonstrate a complete data workflow from raw project information to executive-level reporting.

---

## 2. Technical Architecture

The project follows this architecture:

```text id="y5w8v9"
1. Synthetic data generation
2. Raw CSV output
3. Data cleaning and enrichment
4. Processed CSV output
5. KPI analysis generation
6. SQLite database loading
7. SQL portfolio analysis
8. Power BI dashboard planning
```

This structure is designed to simulate a real-world analytics pipeline used by PMO, operations, or business analysis teams.

---

## 3. Data Pipeline

### Step 1: Generate Synthetic Data

Script:

```text id="39cypu"
src/generate_sample_data.py
```

Output folder:

```text id="6veseg"
data/raw/
```

Generated files:

```text id="dv32wy"
project_master.csv
milestone_tracker.csv
risk_issue_log.csv
budget_control.csv
```

Purpose:

This script creates a realistic synthetic project portfolio without using confidential company data.

It simulates:

* project records
* departments
* project managers
* project status
* budget values
* forecast costs
* project milestones
* project risks
* risk scoring
* schedule health

---

### Step 2: Clean and Enrich Data

Script:

```text id="nl0ubf"
src/clean_portfolio_data.py
```

Input folder:

```text id="56974v"
data/raw/
```

Output folders:

```text id="5ek4nz"
data/processed/
outputs/
```

Generated processed files:

```text id="zm5idq"
project_master_clean.csv
milestone_tracker_clean.csv
risk_issue_log_clean.csv
budget_control_clean.csv
project_portfolio_enriched.csv
```

Generated executive files:

```text id="6ohsp5"
executive_summary.csv
projects_requiring_attention.csv
```

Purpose:

This script transforms raw project data into decision-ready data.

It calculates:

* project delay indicators
* budget overrun indicators
* forecast overrun indicators
* milestone completion metrics
* overdue milestone counts
* risk exposure metrics
* traffic light status
* executive attention flags

---

### Step 3: Generate KPI Analysis

Script:

```text id="j2rnna"
src/portfolio_kpi_analysis.py
```

Output folder:

```text id="iic8of"
outputs/
```

Generated files:

```text id="08u7ew"
portfolio_kpi_summary.csv
department_performance_summary.csv
project_manager_performance_summary.csv
traffic_light_summary.csv
budget_analysis_summary.csv
risk_analysis_summary.csv
top_projects_requiring_attention.csv
```

Purpose:

This script summarizes portfolio performance from different business angles:

* overall portfolio health
* department performance
* project manager performance
* traffic light distribution
* budget performance
* risk exposure
* executive attention priorities

---

### Step 4: Load Data into SQLite

Script:

```text id="hp44w6"
src/load_data_to_sqlite.py
```

Generated local database:

```text id="7jpxn3"
data/pmo_portfolio.db
```

Purpose:

This step loads processed CSV files into a relational database structure.

The SQLite database is generated locally and excluded from Git because it can be recreated.

Run command:

```bash id="u9a3n8"
python src/load_data_to_sqlite.py
```

---

## 4. Main Data Tables

### project_master

This table contains one row per project.

Key columns:

```text id="q113cu"
project_id
project_name
project_type
department
sponsor
project_manager
priority
status
schedule_health
start_date
planned_end_date
actual_end_date
completion_percentage
budget
actual_cost
forecast_cost
```

Business purpose:

This is the core project table. It provides the main project-level information used throughout the portfolio.

---

### milestone_tracker

This table contains project milestone records.

Key columns:

```text id="llg2y0"
milestone_id
project_id
milestone_name
owner
planned_date
actual_date
status
delay_days
```

Business purpose:

This table allows the PMO to monitor execution progress and identify overdue milestones.

Relationship:

```text id="pq0vpu"
project_master.project_id → milestone_tracker.project_id
```

Relationship type:

```text id="97rjc2"
One project can have many milestones.
```

---

### risk_issue_log

This table contains project risk and issue records.

Key columns:

```text id="zdxpuz"
risk_id
project_id
risk_category
risk_description
probability
impact
risk_score
risk_level
risk_owner
mitigation_plan
status
date_identified
```

Business purpose:

This table allows the PMO to monitor risk exposure, high-risk items, escalations, and mitigation planning.

Relationship:

```text id="fxtpgx"
project_master.project_id → risk_issue_log.project_id
```

Relationship type:

```text id="hx2ekt"
One project can have many risks.
```

---

### budget_control

This table contains budget and cost performance data.

Key columns:

```text id="9us5qb"
project_id
project_name
department
project_manager
budget
actual_cost
forecast_cost
budget_variance
forecast_variance
cost_overrun_percentage
budget_status
```

Business purpose:

This table allows the PMO to compare approved budget, actual spend, forecast spend, and overrun behavior.

Relationship:

```text id="bvt8tk"
project_master.project_id → budget_control.project_id
```

Relationship type:

```text id="dzhrzj"
One project has one budget control record.
```

---

### project_portfolio_enriched

This is the main analytical table.

It combines project data, budget indicators, milestone summaries, risk summaries, and executive flags.

Key columns:

```text id="sn01tq"
project_id
project_name
department
project_manager
priority
status
schedule_health
completion_percentage
budget
actual_cost
forecast_cost
is_delayed
is_over_budget
is_forecast_over_budget
overdue_milestones
open_risks
high_risks
escalated_risks
portfolio_risk_exposure
budget_variance_category
risk_exposure_flag
traffic_light_status
requires_executive_attention
```

Business purpose:

This table is optimized for executive reporting and Power BI dashboard creation.

---

## 5. KPI Logic

### Project Delay

A project is considered delayed when its planned end date has passed and it is not completed.

Example field:

```text id="fwcfbi"
is_delayed
```

Business meaning:

This helps identify projects that are behind schedule.

---

### Budget Overrun

A project is considered over budget when:

```text id="yq9vq6"
actual_cost > budget
```

Example field:

```text id="va2k28"
is_over_budget
```

Business meaning:

This identifies projects that have already exceeded approved budget.

---

### Forecast Over Budget

A project is forecasted over budget when:

```text id="febfyo"
forecast_cost > budget
```

Example field:

```text id="7bzgxv"
is_forecast_over_budget
```

Business meaning:

This helps detect future budget problems before they fully occur.

---

### Budget Variance

Budget variance is calculated as:

```text id="azvg1h"
budget - actual_cost
```

Interpretation:

```text id="2xapnf"
Positive variance = under budget
Negative variance = over budget
```

---

### Cost Overrun Percentage

Cost overrun percentage measures how much a project has exceeded budget relative to the approved budget.

Business meaning:

This helps compare overruns across projects of different sizes.

---

## 6. Risk Scoring Model

The risk score is calculated as:

```text id="p22t6y"
Risk Score = Probability × Impact
```

Where:

```text id="bnd866"
Probability = likelihood of the risk occurring
Impact = severity if the risk occurs
```

Risk level classification:

```text id="ujxd40"
1 - 5   = Low Risk
6 - 14  = Medium Risk
15 - 25 = High Risk
```

Business purpose:

This allows risks to be prioritized consistently.

A high-risk project may require escalation, additional monitoring, or leadership review.

---

## 7. Traffic Light Status Logic

The project uses a traffic light model:

```text id="tgdm79"
Green  = On track
Yellow = Requires monitoring
Red    = Requires executive attention
```

A project may be Red when it has one or more serious issues such as:

* high risk exposure
* escalated risks
* overdue milestones
* major delay
* budget overrun
* forecast overrun

Business purpose:

The traffic light model makes project health easy to understand for executives and non-technical stakeholders.

---

## 8. Executive Attention Logic

The field:

```text id="i3h8oj"
requires_executive_attention
```

identifies projects that should be reviewed by leadership.

A project may require executive attention when it has:

* Red traffic light status
* High risk exposure
* Escalated risks
* Budget overrun
* Significant schedule delay
* Multiple overdue milestones

Business purpose:

This helps PMO teams prioritize which projects should be discussed first in executive reviews.

---

## 9. SQL Layer

The SQL layer contains two files:

```text id="f7rl3u"
sql/create_tables.sql
sql/portfolio_queries.sql
```

### create_tables.sql

This file creates the database schema.

It defines:

* table names
* columns
* data types
* primary keys
* foreign key relationships
* indexes

Purpose:

To model the project portfolio data in a structured relational format.

---

### portfolio_queries.sql

This file contains analytical queries for:

* executive overview
* traffic light summary
* department performance
* project manager performance
* budget performance
* risk exposure
* overdue milestone details
* high-risk item details
* data quality validation

Purpose:

To demonstrate business analysis using SQL.

---

## 10. Power BI Layer

Power BI is planned using these files:

```text id="qzi4cz"
powerbi/dashboard_requirements.md
powerbi/build_steps.md
```

Expected final file:

```text id="evpbym"
powerbi/pmo_portfolio_dashboard.pbix
```

The dashboard should include:

* Executive Overview
* Portfolio Health
* Budget Performance
* Risk Management
* Milestone Performance
* Department and PM Performance
* Executive Attention

Purpose:

To convert the processed project data into visual executive reporting.

---

## 11. Data Quality Controls

The project includes validation logic to check:

* missing required fields
* projects without proper IDs
* orphan milestone records
* orphan risk records
* orphan budget records
* completed projects with invalid dates
* inconsistent cost values

Business purpose:

Good reporting depends on reliable data. Data quality checks help prevent inaccurate executive decisions.

---

## 12. How to Run the Full Pipeline

Run these commands in order:

```bash id="b9xxfx"
python -m pip install -r requirements.txt
python src/generate_sample_data.py
python src/clean_portfolio_data.py
python src/portfolio_kpi_analysis.py
python src/load_data_to_sqlite.py
```

Expected result:

* raw datasets are generated
* processed datasets are generated
* KPI output files are generated
* SQLite database is created locally
* data is ready for SQL analysis and Power BI

---

## 13. Why This Project Matters

This project is valuable because it connects business operations with technical execution.

It demonstrates that the builder can:

* understand a business problem
* design a data workflow
* clean and enrich data
* define KPIs
* model data in SQL
* write analytical queries
* plan executive dashboards
* document the project professionally

This makes it relevant for PMO, business analysis, operations, project controls, BI, and digital transformation roles.

---

## 14. Future Technical Improvements

Future improvements could include:

* automated Power BI refresh
* SharePoint or Microsoft Lists integration
* Microsoft Project or Jira integration
* email alerts for Red projects
* predictive risk scoring
* resource capacity planning
* monthly executive report generation
* deployment to a cloud database
* dashboard publishing in Power BI Service

---

## 15. Final Technical Summary

The PMO Project Portfolio Control System is a full business analytics pipeline.

It starts with synthetic project portfolio data, transforms it through Python, models it through SQL and SQLite, and prepares it for Power BI executive reporting.

The project demonstrates a practical combination of project management, data analytics, business intelligence, and automation.
