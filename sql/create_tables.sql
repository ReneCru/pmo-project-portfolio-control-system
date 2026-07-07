-- ============================================================
-- PMO Project Portfolio Control System
-- SQL Table Creation Script
-- ============================================================

-- This script defines the database tables used by the PMO
-- Project Portfolio Control System.
--
-- The structure is designed to support project portfolio analysis,
-- milestone tracking, risk management, budget control, and executive
-- KPI reporting.
--
-- SQL dialect: SQLite-compatible
-- ============================================================


-- ============================================================
-- Drop existing tables
-- ============================================================

DROP TABLE IF EXISTS project_portfolio_enriched;
DROP TABLE IF EXISTS budget_control;
DROP TABLE IF EXISTS risk_issue_log;
DROP TABLE IF EXISTS milestone_tracker;
DROP TABLE IF EXISTS project_master;


-- ============================================================
-- Project Master Table
-- ============================================================

CREATE TABLE project_master (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_type TEXT,
    department TEXT,
    sponsor TEXT,
    project_manager TEXT,
    priority TEXT,
    strategic_alignment TEXT,
    business_impact TEXT,
    status TEXT,
    schedule_health TEXT,
    start_date TEXT,
    planned_end_date TEXT,
    actual_end_date TEXT,
    completion_percentage REAL,
    budget REAL,
    actual_cost REAL,
    forecast_cost REAL,
    budget_variance REAL,
    forecast_variance REAL,
    is_completed INTEGER,
    is_delayed INTEGER,
    is_over_budget INTEGER,
    is_forecast_over_budget INTEGER,
    days_until_due INTEGER,
    project_delay_days INTEGER
);


-- ============================================================
-- Milestone Tracker Table
-- ============================================================

CREATE TABLE milestone_tracker (
    milestone_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    milestone_name TEXT,
    owner TEXT,
    planned_date TEXT,
    actual_date TEXT,
    status TEXT,
    delay_days INTEGER,
    is_completed_milestone INTEGER,
    is_overdue_milestone INTEGER,
    overdue_delay_days INTEGER,

    FOREIGN KEY (project_id) REFERENCES project_master(project_id)
);


-- ============================================================
-- Risk and Issue Log Table
-- ============================================================

CREATE TABLE risk_issue_log (
    risk_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    risk_category TEXT,
    risk_description TEXT,
    probability INTEGER,
    impact INTEGER,
    risk_score INTEGER,
    risk_level TEXT,
    risk_owner TEXT,
    mitigation_plan TEXT,
    status TEXT,
    date_identified TEXT,
    is_open_risk INTEGER,
    is_high_risk INTEGER,
    is_escalated INTEGER,
    open_risk_score INTEGER,

    FOREIGN KEY (project_id) REFERENCES project_master(project_id)
);


-- ============================================================
-- Budget Control Table
-- ============================================================

CREATE TABLE budget_control (
    project_id TEXT PRIMARY KEY,
    project_name TEXT,
    department TEXT,
    project_manager TEXT,
    budget REAL,
    actual_cost REAL,
    forecast_cost REAL,
    budget_variance REAL,
    forecast_variance REAL,
    cost_overrun_percentage REAL,
    budget_status TEXT,

    FOREIGN KEY (project_id) REFERENCES project_master(project_id)
);


-- ============================================================
-- Enriched Project Portfolio Table
-- ============================================================

CREATE TABLE project_portfolio_enriched (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_type TEXT,
    department TEXT,
    sponsor TEXT,
    project_manager TEXT,
    priority TEXT,
    strategic_alignment TEXT,
    business_impact TEXT,
    status TEXT,
    schedule_health TEXT,
    start_date TEXT,
    planned_end_date TEXT,
    actual_end_date TEXT,
    completion_percentage REAL,
    budget REAL,
    actual_cost REAL,
    forecast_cost REAL,
    is_completed INTEGER,
    is_delayed INTEGER,
    is_over_budget INTEGER,
    is_forecast_over_budget INTEGER,
    days_until_due INTEGER,
    project_delay_days INTEGER,

    total_milestones INTEGER,
    completed_milestones INTEGER,
    overdue_milestones INTEGER,
    total_milestone_delay_days INTEGER,
    total_overdue_delay_days INTEGER,
    milestone_completion_rate REAL,

    total_risks INTEGER,
    open_risks INTEGER,
    high_risks INTEGER,
    escalated_risks INTEGER,
    portfolio_risk_exposure INTEGER,
    max_risk_score INTEGER,

    budget_variance REAL,
    forecast_variance REAL,
    cost_overrun_percentage REAL,
    budget_status TEXT,

    budget_variance_category TEXT,
    risk_exposure_flag TEXT,
    traffic_light_status TEXT,
    requires_executive_attention INTEGER
);


-- ============================================================
-- Indexes for Query Performance
-- ============================================================

CREATE INDEX idx_project_master_department
ON project_master(department);

CREATE INDEX idx_project_master_project_manager
ON project_master(project_manager);

CREATE INDEX idx_project_master_status
ON project_master(status);

CREATE INDEX idx_project_master_schedule_health
ON project_master(schedule_health);

CREATE INDEX idx_milestone_project_id
ON milestone_tracker(project_id);

CREATE INDEX idx_milestone_status
ON milestone_tracker(status);

CREATE INDEX idx_risk_project_id
ON risk_issue_log(project_id);

CREATE INDEX idx_risk_level
ON risk_issue_log(risk_level);

CREATE INDEX idx_risk_status
ON risk_issue_log(status);

CREATE INDEX idx_budget_status
ON budget_control(budget_status);

CREATE INDEX idx_enriched_department
ON project_portfolio_enriched(department);

CREATE INDEX idx_enriched_project_manager
ON project_portfolio_enriched(project_manager);

CREATE INDEX idx_enriched_traffic_light
ON project_portfolio_enriched(traffic_light_status);

CREATE INDEX idx_enriched_risk_exposure
ON project_portfolio_enriched(risk_exposure_flag);

CREATE INDEX idx_enriched_budget_category
ON project_portfolio_enriched(budget_variance_category);


-- ============================================================
-- End of script
-- ============================================================
