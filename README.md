# PMO Project Portfolio Control System

A professional PMO analytics and portfolio control system built with Python, SQL, SQLite, and Power BI planning documentation.

This project simulates how a PMO or project controls team can monitor project portfolio health, budget variance, milestone delays, risk exposure, and executive attention priorities across multiple business areas.

---

## Project Objective

The objective of this project is to build a Project Portfolio Control System that allows a PMO, Project Manager, Business Analyst, or Operations team to track and analyze project performance across departments.

The system provides visibility into:

* Project status
* Schedule delays
* Budget variance
* Forecast cost overruns
* Milestone performance
* Risk exposure
* Executive traffic light status
* Projects requiring leadership attention

---

## Business Problem

Many organizations manage projects across departments using disconnected spreadsheets, emails, meetings, and manual reports.

This creates problems such as:

* Lack of centralized project visibility
* Late detection of delayed projects
* Poor budget variance control
* Weak risk prioritization
* Inconsistent executive reporting
* No single source of truth for portfolio health

This project solves that problem by creating a structured PMO control system using data generation, data cleaning, KPI analysis, SQL modeling, and Power BI dashboard planning.

---

## Tools and Technologies

* Python
* pandas
* NumPy
* Faker
* SQLite
* SQL
* Power BI
* CSV datasets
* Markdown documentation
* GitHub Codespaces

---

## Project Architecture

```text
Synthetic Data Generation
        ↓
Raw CSV Datasets
        ↓
Data Cleaning and Enrichment
        ↓
Processed KPI-Ready Datasets
        ↓
Portfolio KPI Analysis
        ↓
SQLite Database Loading
        ↓
SQL Portfolio Queries
        ↓
Power BI Dashboard Design
```

---

## Repository Structure

```text
pmo-project-portfolio-control-system/
│
├── data/
│   ├── raw/
│   │   ├── project_master.csv
│   │   ├── milestone_tracker.csv
│   │   ├── risk_issue_log.csv
│   │   └── budget_control.csv
│   │
│   └── processed/
│       ├── project_master_clean.csv
│       ├── milestone_tracker_clean.csv
│       ├── risk_issue_log_clean.csv
│       ├── budget_control_clean.csv
│       └── project_portfolio_enriched.csv
│
├── docs/
│   ├── business_case.md
│   ├── kpi_dictionary.md
│   ├── risk_scoring_model.md
│   └── pmo_process_flow.md
│
├── outputs/
│   ├── executive_summary.csv
│   ├── projects_requiring_attention.csv
│   ├── portfolio_kpi_summary.csv
│   ├── department_performance_summary.csv
│   ├── project_manager_performance_summary.csv
│   ├── traffic_light_summary.csv
│   ├── budget_analysis_summary.csv
│   ├── risk_analysis_summary.csv
│   └── top_projects_requiring_attention.csv
│
├── powerbi/
│   ├── dashboard_requirements.md
│   ├── build_steps.md
│   └── pmo_portfolio_dashboard.pbix
│
├── sql/
│   ├── create_tables.sql
│   └── portfolio_queries.sql
│
├── src/
│   ├── generate_sample_data.py
│   ├── clean_portfolio_data.py
│   ├── portfolio_kpi_analysis.py
│   └── load_data_to_sqlite.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Main Python Scripts

### `generate_sample_data.py`

Generates synthetic PMO portfolio datasets.

Created files:

* `data/raw/project_master.csv`
* `data/raw/milestone_tracker.csv`
* `data/raw/risk_issue_log.csv`
* `data/raw/budget_control.csv`

This script simulates project master records, milestones, risks, issues, budget control, schedule health, project completion, and risk scoring.

---

### `clean_portfolio_data.py`

Cleans and enriches the raw datasets.

Created files:

* `data/processed/project_master_clean.csv`
* `data/processed/milestone_tracker_clean.csv`
* `data/processed/risk_issue_log_clean.csv`
* `data/processed/budget_control_clean.csv`
* `data/processed/project_portfolio_enriched.csv`
* `outputs/executive_summary.csv`
* `outputs/projects_requiring_attention.csv`

This script creates analytical fields such as:

* `is_delayed`
* `is_over_budget`
* `is_forecast_over_budget`
* `project_delay_days`
* `overdue_milestones`
* `portfolio_risk_exposure`
* `budget_variance_category`
* `risk_exposure_flag`
* `traffic_light_status`
* `requires_executive_attention`

---

### `portfolio_kpi_analysis.py`

Calculates portfolio-level KPI summaries and analytical reports.

Created files:

* `outputs/portfolio_kpi_summary.csv`
* `outputs/department_performance_summary.csv`
* `outputs/project_manager_performance_summary.csv`
* `outputs/traffic_light_summary.csv`
* `outputs/budget_analysis_summary.csv`
* `outputs/risk_analysis_summary.csv`
* `outputs/top_projects_requiring_attention.csv`

---

### `load_data_to_sqlite.py`

Loads processed CSV datasets into a SQLite database.

Generated database:

* `data/pmo_portfolio.db`

The database is generated locally and excluded from Git tracking because it can be recreated by running the script.

---

## SQL Components

### `create_tables.sql`

Defines the SQLite-compatible database schema.

Tables created:

* `project_master`
* `milestone_tracker`
* `risk_issue_log`
* `budget_control`
* `project_portfolio_enriched`

### `portfolio_queries.sql`

Contains SQL queries for:

* Portfolio executive overview
* Traffic light summary
* Department performance
* Project manager performance
* Budget performance
* Risk exposure
* Overdue milestones
* High-risk items
* Projects requiring executive attention
* Data quality validation

---

## Key KPIs

The system tracks:

* Total projects
* Active projects
* Completed projects
* Delayed projects
* Projects over budget
* Forecast over budget projects
* Projects requiring executive attention
* Total portfolio budget
* Total actual cost
* Total forecast cost
* Total budget variance
* Average completion percentage
* Total open risks
* High-risk projects
* Escalated risks
* Portfolio risk exposure
* Overdue milestones
* Executive attention rate

---

## Risk Scoring Model

The system uses a simple PMO risk scoring model:

```text
Risk Score = Probability × Impact
```

Risk classification:

```text
1 - 5   = Low Risk
6 - 14  = Medium Risk
15 - 25 = High Risk
```

This allows the portfolio to identify projects requiring monitoring, mitigation, escalation, or executive review.

---

## Executive Traffic Light Logic

Projects are classified using a traffic light model:

```text
Green  = Project is on track
Yellow = Project requires monitoring
Red    = Project requires executive attention
```

A project may be classified as Red if it is delayed, over budget, has high risks, escalated risks, or multiple overdue milestones.

---

## How to Run the Project

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Generate synthetic datasets:

```bash
python src/generate_sample_data.py
```

Clean and enrich datasets:

```bash
python src/clean_portfolio_data.py
```

Generate KPI analysis outputs:

```bash
python src/portfolio_kpi_analysis.py
```

Load processed data into SQLite:

```bash
python src/load_data_to_sqlite.py
```

---

## Power BI Dashboard

The Power BI dashboard is planned using:

* `powerbi/dashboard_requirements.md`
* `powerbi/build_steps.md`

Expected final Power BI file:

```text
powerbi/pmo_portfolio_dashboard.pbix
```

The dashboard should include pages for:

* Executive Overview
* Portfolio Health
* Budget Performance
* Risk Management
* Milestone Performance
* Department and PM Performance
* Executive Attention

---

## Business Value

This project demonstrates how project management, data analysis, SQL, Python automation, and business intelligence can be combined to create a PMO control system.

It supports better decision-making by helping leadership identify:

* Which projects are in trouble
* Which departments have the highest risk exposure
* Which projects are over budget
* Which milestones are overdue
* Which risks require escalation
* Which projects need executive review first

---

## Professional Portfolio Relevance

This project is relevant for roles such as:

* Project Manager
* PMO Analyst
* Business Analyst
* Operations Analyst
* Project Controls Analyst
* BI Analyst
* Digital Transformation Analyst
* Supply Chain Analyst
* Process Improvement Analyst

It demonstrates practical experience in:

* Project portfolio control
* KPI design
* Risk scoring
* Budget variance analysis
* Data cleaning
* SQL analysis
* Executive dashboard planning
* Business documentation
* Python automation

---

## Current Status

Completed:

* Business case documentation
* KPI dictionary
* Risk scoring model
* PMO process flow
* Synthetic data generation
* Data cleaning and enrichment
* KPI analysis outputs
* SQLite database loading script
* SQL table creation script
* SQL portfolio analysis queries
* Power BI dashboard requirements
* Power BI build guide

Pending:

* Build the Power BI `.pbix` dashboard manually in Power BI Desktop
* Export dashboard screenshots
* Add screenshots to README
* Create final project explanation for LinkedIn
* Create interview explanation
* Create final project exam with answers

---

## Future Improvements

Potential future enhancements:

* Automated email alerts for high-risk projects
* SharePoint or Microsoft Lists integration
* Predictive project health scoring
* Resource capacity planning
* Project prioritization scoring
* Monthly executive report automation
* Power BI Service scheduled refresh
* Integration with Microsoft Project, Jira, or Smartsheet
