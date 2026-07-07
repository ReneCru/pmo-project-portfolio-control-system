# Interview Explanation: PMO Project Portfolio Control System

## 1. Short Project Pitch

I built a PMO Project Portfolio Control System using Python, SQL, SQLite, and Power BI planning documentation.

The project simulates how a PMO or project controls team can monitor project health, budget variance, milestone delays, risk exposure, and executive attention priorities across multiple departments.

The goal was to create a structured data pipeline that turns project information into executive-level insights.

---

## 2. What Business Problem Does This Solve?

Many companies manage project portfolios through disconnected spreadsheets, manual updates, emails, and status meetings.

That creates several problems:

* Leadership does not have a single source of truth.
* Delayed projects are detected too late.
* Budget overruns are not always visible early.
* Risks are not prioritized consistently.
* PMO reporting becomes manual and reactive.

This project solves that by creating an automated portfolio control system where data is generated, cleaned, analyzed, modeled in SQL, and prepared for Power BI reporting.

---

## 3. Technologies Used

The project uses:

* Python for data generation, cleaning, and KPI analysis.
* pandas for data manipulation.
* NumPy and Faker for synthetic dataset generation.
* SQLite for database modeling.
* SQL for portfolio analysis queries.
* Power BI planning documentation for dashboard design.
* GitHub for version control and portfolio presentation.

---

## 4. Project Architecture

The project follows this flow:

```text id="bv0o1f"
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
Power BI Dashboard Planning
```

This structure reflects a realistic business analytics workflow.

---

## 5. Main Python Scripts

### generate_sample_data.py

This script creates synthetic PMO data.

It generates:

* Project master data
* Milestone tracking data
* Risk and issue logs
* Budget control records

The goal is to simulate a realistic project portfolio without using confidential company data.

---

### clean_portfolio_data.py

This script cleans and enriches the raw datasets.

It creates calculated fields such as:

* is_delayed
* is_over_budget
* is_forecast_over_budget
* project_delay_days
* overdue_milestones
* portfolio_risk_exposure
* traffic_light_status
* requires_executive_attention

This step is important because raw data alone is not enough for business reporting. It needs to be transformed into decision-ready information.

---

### portfolio_kpi_analysis.py

This script creates executive summary outputs.

It generates reports by:

* Portfolio level
* Department
* Project manager
* Traffic light status
* Budget performance
* Risk exposure
* Projects requiring executive attention

This allows leadership to identify which areas need attention first.

---

### load_data_to_sqlite.py

This script loads the processed CSV files into a SQLite database.

The reason for this step is to show that the project can move beyond flat files and operate like a structured database system.

---

## 6. SQL Explanation

The SQL part has two main files:

### create_tables.sql

This file creates the database tables:

* project_master
* milestone_tracker
* risk_issue_log
* budget_control
* project_portfolio_enriched

It defines the structure of the database and the relationships between the main project table and the supporting detail tables.

### portfolio_queries.sql

This file contains analytical SQL queries for:

* Executive portfolio overview
* Department performance
* Project manager performance
* Budget variance analysis
* Risk exposure analysis
* Overdue milestone tracking
* High-risk item detail
* Data quality validation

The purpose is to demonstrate that I can analyze business performance using SQL, not only Python or Power BI.

---

## 7. Power BI Explanation

The Power BI dashboard is planned to show:

* Executive Overview
* Portfolio Health
* Budget Performance
* Risk Management
* Milestone Performance
* Department and PM Performance
* Executive Attention

The dashboard is designed to help leaders answer:

* Which projects are in trouble?
* Which projects are over budget?
* Which departments have the most risk?
* Which milestones are overdue?
* Which projects need executive review first?

The Power BI `.pbix` file is pending manual build in Power BI Desktop.

---

## 8. Risk Scoring Logic

The project uses a simple risk scoring model:

```text id="quepnh"
Risk Score = Probability × Impact
```

Risk levels are classified as:

```text id="cfrnfx"
1 - 5   = Low Risk
6 - 14  = Medium Risk
15 - 25 = High Risk
```

This allows the system to identify projects with higher risk exposure and prioritize executive attention.

---

## 9. Traffic Light Logic

Projects are classified with a traffic light model:

```text id="2am7uh"
Green  = On track
Yellow = Requires monitoring
Red    = Requires executive attention
```

A project may become Red when it has serious schedule delays, budget overruns, high risks, escalated risks, or overdue milestones.

This makes the portfolio easier to read for non-technical stakeholders.

---

## 10. Example Interview Answer: What Did You Build?

I built a PMO Project Portfolio Control System that uses Python, SQL, SQLite, and Power BI planning documentation to monitor project health across a simulated project portfolio.

The system generates synthetic project data, cleans and enriches it, calculates KPIs, loads the processed data into a SQLite database, and provides SQL queries for executive-level portfolio analysis.

The purpose is to help leadership identify delayed projects, budget overruns, high-risk projects, overdue milestones, and projects requiring executive attention.

---

## 11. Example Interview Answer: Why Did You Build This?

I built this project because many organizations struggle with project visibility. In real business environments, project data is often spread across spreadsheets, emails, and manual reports.

I wanted to simulate a more structured PMO reporting process where data flows from raw inputs into clean datasets, KPI analysis, SQL reporting, and Power BI dashboard design.

This project connects project management, business analysis, data analytics, and automation.

---

## 12. Example Interview Answer: What Was the Most Valuable Part?

The most valuable part was building the complete workflow from data generation to executive reporting.

Instead of only creating a dashboard, I built the supporting data pipeline behind it:

* synthetic data generation
* data cleaning
* KPI logic
* risk scoring
* SQL database loading
* analytical SQL queries
* Power BI dashboard requirements

That makes the project stronger because it shows both technical execution and business understanding.

---

## 13. Example Interview Answer: How Would This Help a Business?

This system would help a business improve project governance and visibility.

A PMO or operations team could use it to detect project delays earlier, identify projects with high risk exposure, track budget overruns, and prioritize leadership attention.

It would reduce manual reporting and help leaders focus on the projects that need action first.

---

## 14. Example Interview Answer: What Would You Improve Next?

The next improvements would be:

* Build the full Power BI dashboard.
* Add automated alerts for high-risk projects.
* Add resource capacity planning.
* Add predictive project health scoring.
* Connect the model to Microsoft Lists, SharePoint, Jira, or Microsoft Project.
* Add Power BI Service scheduled refresh.
* Create monthly executive report automation.

These improvements would make the system closer to a real enterprise PMO solution.

---

## 15. Simple Spanish Explanation

Construí un sistema de control de portafolio de proyectos para una PMO.

El objetivo es ayudar a visualizar qué proyectos están atrasados, cuáles están sobre presupuesto, cuáles tienen riesgos altos, cuáles tienen milestones vencidos y cuáles necesitan atención ejecutiva.

El proyecto usa Python para generar, limpiar y analizar datos; SQL y SQLite para modelar la información; y documentación de Power BI para planear el dashboard ejecutivo.

Es un proyecto fuerte porque combina gestión de proyectos, análisis de datos, automatización, SQL, documentación de negocio y visualización ejecutiva.

---

## 16. Strong Resume Bullet

Built a PMO Project Portfolio Control System using Python, SQL, SQLite, and Power BI planning documentation to monitor project health, budget variance, milestone delays, risk exposure, and executive attention priorities across a simulated enterprise project portfolio.

---

## 17. LinkedIn Short Description

I built a PMO Project Portfolio Control System to simulate how project and operations teams can monitor portfolio health, budget variance, risk exposure, milestone delays, and executive attention priorities using Python, SQL, SQLite, and Power BI planning documentation.

This project helped me practice data generation, data cleaning, KPI analysis, database modeling, SQL reporting, and executive dashboard design from a project management and business analytics perspective.

---

## 18. Key Skills Demonstrated

This project demonstrates:

* Project portfolio management
* PMO reporting
* KPI design
* Risk scoring
* Budget variance analysis
* Data cleaning
* Python automation
* SQL analysis
* SQLite database modeling
* Power BI dashboard planning
* Executive reporting
* Business documentation
* Analytical thinking

---

## 19. Interview Closing Statement

This project represents the type of work I want to continue doing: combining business operations, project management, data analytics, and automation to improve visibility and decision-making.

It shows that I can understand a business problem, design a data structure, build the analytical pipeline, and prepare the reporting layer for leadership.
