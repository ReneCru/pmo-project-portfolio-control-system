# Project Completion Checklist: PMO Project Portfolio Control System

## 1. Purpose

This checklist tracks the completion status of the PMO Project Portfolio Control System.

It is used to validate that the project includes business documentation, Python scripts, generated datasets, processed datasets, KPI outputs, SQL scripts, Power BI planning documentation, and final portfolio deliverables.

---

## 2. Core Project Components

| Component                    | Status    | Notes                                       |
| ---------------------------- | --------- | ------------------------------------------- |
| README.md                    | Completed | Professional project overview created       |
| requirements.txt             | Completed | Python dependencies defined                 |
| .gitignore                   | Completed | Generated database and cache files excluded |
| Business Case                | Completed | Located in docs/business_case.md            |
| KPI Dictionary               | Completed | Located in docs/kpi_dictionary.md           |
| Risk Scoring Model           | Completed | Located in docs/risk_scoring_model.md       |
| PMO Process Flow             | Completed | Located in docs/pmo_process_flow.md         |
| Project Completion Checklist | Completed | Current document                            |

---

## 3. Python Scripts

| Script                        | Status    | Purpose                                    |
| ----------------------------- | --------- | ------------------------------------------ |
| src/generate_sample_data.py   | Completed | Generates synthetic PMO portfolio datasets |
| src/clean_portfolio_data.py   | Completed | Cleans and enriches raw datasets           |
| src/portfolio_kpi_analysis.py | Completed | Generates KPI analysis outputs             |
| src/load_data_to_sqlite.py    | Completed | Loads processed CSV files into SQLite      |

---

## 4. Raw Datasets

Expected location:

```text
data/raw/
```

Expected files:

| File                  | Status    |
| --------------------- | --------- |
| project_master.csv    | Completed |
| milestone_tracker.csv | Completed |
| risk_issue_log.csv    | Completed |
| budget_control.csv    | Completed |

---

## 5. Processed Datasets

Expected location:

```text
data/processed/
```

Expected files:

| File                           | Status    |
| ------------------------------ | --------- |
| project_master_clean.csv       | Completed |
| milestone_tracker_clean.csv    | Completed |
| risk_issue_log_clean.csv       | Completed |
| budget_control_clean.csv       | Completed |
| project_portfolio_enriched.csv | Completed |

---

## 6. Executive Outputs

Expected location:

```text
outputs/
```

Expected files:

| File                                    | Status    |
| --------------------------------------- | --------- |
| executive_summary.csv                   | Completed |
| projects_requiring_attention.csv        | Completed |
| portfolio_kpi_summary.csv               | Completed |
| department_performance_summary.csv      | Completed |
| project_manager_performance_summary.csv | Completed |
| traffic_light_summary.csv               | Completed |
| budget_analysis_summary.csv             | Completed |
| risk_analysis_summary.csv               | Completed |
| top_projects_requiring_attention.csv    | Completed |

---

## 7. SQL Components

Expected location:

```text
sql/
```

| File                  | Status    | Purpose                             |
| --------------------- | --------- | ----------------------------------- |
| create_tables.sql     | Completed | Defines SQLite table structure      |
| portfolio_queries.sql | Completed | Contains portfolio analysis queries |

Expected SQLite database:

```text
data/pmo_portfolio.db
```

Status:

```text
Generated locally. Not tracked in Git.
```

Reason:

The database can be recreated by running:

```bash
python src/load_data_to_sqlite.py
```

---

## 8. Power BI Components

Expected location:

```text
powerbi/
```

| File                         | Status    | Purpose                                    |
| ---------------------------- | --------- | ------------------------------------------ |
| dashboard_requirements.md    | Completed | Defines dashboard requirements             |
| build_steps.md               | Completed | Provides practical build instructions      |
| pmo_portfolio_dashboard.pbix | Pending   | Must be built manually in Power BI Desktop |

Power BI work pending:

* Load processed CSV files
* Create relationships
* Create DAX measures
* Build dashboard pages
* Save final `.pbix` file
* Export screenshots
* Add screenshots to README

---

## 9. Validation Commands

Run these commands before closing the project.

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Generate raw datasets

```bash
python src/generate_sample_data.py
```

### Clean and enrich datasets

```bash
python src/clean_portfolio_data.py
```

### Generate KPI outputs

```bash
python src/portfolio_kpi_analysis.py
```

### Load data into SQLite

```bash
python src/load_data_to_sqlite.py
```

---

## 10. File Validation Commands

### Validate raw data

```bash
ls data/raw
```

Expected files:

```text
project_master.csv
milestone_tracker.csv
risk_issue_log.csv
budget_control.csv
```

### Validate processed data

```bash
ls data/processed
```

Expected files:

```text
project_master_clean.csv
milestone_tracker_clean.csv
risk_issue_log_clean.csv
budget_control_clean.csv
project_portfolio_enriched.csv
```

### Validate outputs

```bash
ls outputs
```

Expected files:

```text
executive_summary.csv
projects_requiring_attention.csv
portfolio_kpi_summary.csv
department_performance_summary.csv
project_manager_performance_summary.csv
traffic_light_summary.csv
budget_analysis_summary.csv
risk_analysis_summary.csv
top_projects_requiring_attention.csv
```

---

## 11. Data Quality Validation

Run this validation after loading the SQLite database:

```bash
python - <<'PY'
import sqlite3
import pandas as pd

connection = sqlite3.connect("data/pmo_portfolio.db")

validation_df = pd.read_sql_query(
    """
    SELECT
        'milestone_tracker' AS table_name,
        COUNT(*) AS orphan_records
    FROM milestone_tracker m
    LEFT JOIN project_master p
        ON m.project_id = p.project_id
    WHERE p.project_id IS NULL

    UNION ALL

    SELECT
        'risk_issue_log' AS table_name,
        COUNT(*) AS orphan_records
    FROM risk_issue_log r
    LEFT JOIN project_master p
        ON r.project_id = p.project_id
    WHERE p.project_id IS NULL

    UNION ALL

    SELECT
        'budget_control' AS table_name,
        COUNT(*) AS orphan_records
    FROM budget_control b
    LEFT JOIN project_master p
        ON b.project_id = p.project_id
    WHERE p.project_id IS NULL;
    """,
    connection,
)

print(validation_df.to_string(index=False))
connection.close()
PY
```

Expected result:

```text
orphan_records = 0
```

for all tables.

---

## 12. Git Validation

Before pushing, run:

```bash
git status
```

The repository should not track:

```text
data/pmo_portfolio.db
__pycache__/
*.pyc
.env
.venv/
```

The SQLite database should remain local because it can be regenerated.

---

## 13. Final Pending Deliverables

The following items remain pending before the project is fully closed:

1. Build Power BI dashboard in Power BI Desktop.
2. Save final file as `powerbi/pmo_portfolio_dashboard.pbix`.
3. Export dashboard screenshots.
4. Add screenshots to README.
5. Write LinkedIn project post.
6. Write interview explanation.
7. Create final exam with answers.
8. Review full repository structure.
9. Final GitHub polish.

---

## 14. Final Project Status

Current status:

```text
Core Python, SQL, documentation, and data pipeline completed.
Power BI dashboard pending manual build.
Final portfolio presentation assets pending.
```

This project is ready for Power BI dashboard construction and final portfolio packaging.
