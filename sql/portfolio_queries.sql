-- ============================================================
-- PMO Project Portfolio Control System
-- SQL Portfolio Analysis Queries
-- ============================================================
--
-- SQL dialect: SQLite-compatible
--
-- These queries analyze portfolio performance, budget control,
-- schedule health, milestone delays, risk exposure, and executive
-- attention priorities.
-- ============================================================


-- ============================================================
-- 1. Portfolio Executive Overview
-- ============================================================

SELECT
    COUNT(*) AS total_projects,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_projects,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_projects,
    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS delayed_projects,
    SUM(CASE WHEN is_over_budget = 1 THEN 1 ELSE 0 END) AS projects_over_budget,
    SUM(CASE WHEN is_forecast_over_budget = 1 THEN 1 ELSE 0 END) AS forecast_over_budget_projects,
    SUM(CASE WHEN requires_executive_attention = 1 THEN 1 ELSE 0 END) AS projects_requiring_attention,
    ROUND(SUM(budget), 2) AS total_portfolio_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost,
    ROUND(SUM(forecast_cost), 2) AS total_forecast_cost,
    ROUND(SUM(budget_variance), 2) AS total_budget_variance,
    ROUND(AVG(completion_percentage), 2) AS average_completion_percentage
FROM project_portfolio_enriched;


-- ============================================================
-- 2. Traffic Light Portfolio Summary
-- ============================================================

SELECT
    traffic_light_status,
    COUNT(*) AS total_projects,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM project_portfolio_enriched), 2) AS portfolio_percentage,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost,
    SUM(open_risks) AS total_open_risks,
    SUM(high_risks) AS total_high_risks,
    SUM(overdue_milestones) AS total_overdue_milestones,
    ROUND(AVG(completion_percentage), 2) AS average_completion_percentage
FROM project_portfolio_enriched
GROUP BY traffic_light_status
ORDER BY
    CASE traffic_light_status
        WHEN 'Red' THEN 1
        WHEN 'Yellow' THEN 2
        WHEN 'Green' THEN 3
        ELSE 4
    END;


-- ============================================================
-- 3. Department Performance Summary
-- ============================================================

SELECT
    department,
    COUNT(*) AS total_projects,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_projects,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_projects,
    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS delayed_projects,
    SUM(CASE WHEN is_over_budget = 1 THEN 1 ELSE 0 END) AS over_budget_projects,
    SUM(CASE WHEN requires_executive_attention = 1 THEN 1 ELSE 0 END) AS projects_requiring_attention,
    ROUND(AVG(completion_percentage), 2) AS average_completion_percentage,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost,
    ROUND(SUM(budget_variance), 2) AS total_budget_variance,
    SUM(open_risks) AS total_open_risks,
    SUM(high_risks) AS total_high_risks,
    SUM(escalated_risks) AS total_escalated_risks,
    SUM(overdue_milestones) AS total_overdue_milestones,
    SUM(portfolio_risk_exposure) AS total_risk_exposure
FROM project_portfolio_enriched
GROUP BY department
ORDER BY projects_requiring_attention DESC, total_risk_exposure DESC, total_budget DESC;


-- ============================================================
-- 4. Project Manager Performance Summary
-- ============================================================

SELECT
    project_manager,
    COUNT(*) AS total_projects,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_projects,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_projects,
    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS delayed_projects,
    SUM(CASE WHEN is_over_budget = 1 THEN 1 ELSE 0 END) AS over_budget_projects,
    SUM(CASE WHEN requires_executive_attention = 1 THEN 1 ELSE 0 END) AS projects_requiring_attention,
    ROUND(AVG(completion_percentage), 2) AS average_completion_percentage,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost,
    ROUND(SUM(budget_variance), 2) AS total_budget_variance,
    SUM(open_risks) AS total_open_risks,
    SUM(high_risks) AS total_high_risks,
    SUM(overdue_milestones) AS total_overdue_milestones,
    SUM(portfolio_risk_exposure) AS total_risk_exposure
FROM project_portfolio_enriched
GROUP BY project_manager
ORDER BY projects_requiring_attention DESC, total_risk_exposure DESC, total_projects DESC;


-- ============================================================
-- 5. Top Projects Requiring Executive Attention
-- ============================================================

SELECT
    project_id,
    project_name,
    department,
    project_manager,
    priority,
    status,
    traffic_light_status,
    schedule_health,
    completion_percentage,
    budget,
    actual_cost,
    budget_variance,
    cost_overrun_percentage,
    project_delay_days,
    overdue_milestones,
    high_risks,
    escalated_risks,
    portfolio_risk_exposure,
    (
        high_risks * 5
        + escalated_risks * 5
        + overdue_milestones * 3
        + is_over_budget * 4
        + is_delayed * 4
        + cost_overrun_percentage
    ) AS attention_score
FROM project_portfolio_enriched
WHERE requires_executive_attention = 1
ORDER BY attention_score DESC
LIMIT 15;


-- ============================================================
-- 6. Budget Performance by Category
-- ============================================================

SELECT
    budget_variance_category,
    COUNT(*) AS total_projects,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost,
    ROUND(SUM(forecast_cost), 2) AS total_forecast_cost,
    ROUND(SUM(budget_variance), 2) AS total_budget_variance,
    ROUND(SUM(forecast_variance), 2) AS total_forecast_variance,
    ROUND(AVG(cost_overrun_percentage), 2) AS average_cost_overrun_percentage,
    SUM(CASE WHEN requires_executive_attention = 1 THEN 1 ELSE 0 END) AS projects_requiring_attention
FROM project_portfolio_enriched
GROUP BY budget_variance_category
ORDER BY projects_requiring_attention DESC, total_actual_cost DESC;


-- ============================================================
-- 7. Top Projects Over Budget
-- ============================================================

SELECT
    project_id,
    project_name,
    department,
    project_manager,
    priority,
    status,
    budget,
    actual_cost,
    budget_variance,
    cost_overrun_percentage,
    traffic_light_status
FROM project_portfolio_enriched
WHERE is_over_budget = 1
ORDER BY cost_overrun_percentage DESC, actual_cost DESC
LIMIT 15;


-- ============================================================
-- 8. Forecast Over Budget Projects
-- ============================================================

SELECT
    project_id,
    project_name,
    department,
    project_manager,
    priority,
    status,
    budget,
    actual_cost,
    forecast_cost,
    forecast_variance,
    traffic_light_status
FROM project_portfolio_enriched
WHERE is_forecast_over_budget = 1
ORDER BY forecast_variance ASC, forecast_cost DESC
LIMIT 15;


-- ============================================================
-- 9. Risk Exposure by Department
-- ============================================================

SELECT
    department,
    COUNT(*) AS total_projects,
    SUM(open_risks) AS total_open_risks,
    SUM(high_risks) AS total_high_risks,
    SUM(escalated_risks) AS total_escalated_risks,
    SUM(portfolio_risk_exposure) AS total_risk_exposure,
    ROUND(AVG(max_risk_score), 2) AS average_max_risk_score,
    SUM(CASE WHEN risk_exposure_flag = 'High' THEN 1 ELSE 0 END) AS high_exposure_projects
FROM project_portfolio_enriched
GROUP BY department
ORDER BY total_risk_exposure DESC, total_high_risks DESC;


-- ============================================================
-- 10. High Risk Items Detail
-- ============================================================

SELECT
    r.risk_id,
    r.project_id,
    p.project_name,
    p.department,
    p.project_manager,
    p.priority,
    r.risk_category,
    r.risk_description,
    r.probability,
    r.impact,
    r.risk_score,
    r.risk_level,
    r.status AS risk_status,
    r.risk_owner,
    r.mitigation_plan,
    r.date_identified
FROM risk_issue_log r
LEFT JOIN project_master p
    ON r.project_id = p.project_id
WHERE r.risk_level = 'High'
ORDER BY r.risk_score DESC, p.priority, p.department;


-- ============================================================
-- 11. Overdue Milestones Detail
-- ============================================================

SELECT
    m.milestone_id,
    m.project_id,
    p.project_name,
    p.department,
    p.project_manager,
    p.priority,
    m.milestone_name,
    m.owner,
    m.planned_date,
    m.actual_date,
    m.status AS milestone_status,
    m.delay_days
FROM milestone_tracker m
LEFT JOIN project_master p
    ON m.project_id = p.project_id
WHERE m.is_overdue_milestone = 1
ORDER BY m.delay_days DESC, p.department, p.project_manager;


-- ============================================================
-- 12. Milestone Performance by Department
-- ============================================================

SELECT
    p.department,
    COUNT(m.milestone_id) AS total_milestones,
    SUM(CASE WHEN m.is_completed_milestone = 1 THEN 1 ELSE 0 END) AS completed_milestones,
    SUM(CASE WHEN m.is_overdue_milestone = 1 THEN 1 ELSE 0 END) AS overdue_milestones,
    ROUND(
        SUM(CASE WHEN m.is_completed_milestone = 1 THEN 1 ELSE 0 END) * 100.0
        / COUNT(m.milestone_id),
        2
    ) AS milestone_completion_rate,
    SUM(m.delay_days) AS total_delay_days
FROM milestone_tracker m
LEFT JOIN project_master p
    ON m.project_id = p.project_id
GROUP BY p.department
ORDER BY overdue_milestones DESC, total_delay_days DESC;


-- ============================================================
-- 13. Portfolio Health by Priority
-- ============================================================

SELECT
    priority,
    COUNT(*) AS total_projects,
    SUM(CASE WHEN traffic_light_status = 'Red' THEN 1 ELSE 0 END) AS red_projects,
    SUM(CASE WHEN traffic_light_status = 'Yellow' THEN 1 ELSE 0 END) AS yellow_projects,
    SUM(CASE WHEN traffic_light_status = 'Green' THEN 1 ELSE 0 END) AS green_projects,
    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS delayed_projects,
    SUM(CASE WHEN is_over_budget = 1 THEN 1 ELSE 0 END) AS over_budget_projects,
    SUM(high_risks) AS total_high_risks,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(AVG(completion_percentage), 2) AS average_completion_percentage
FROM project_portfolio_enriched
GROUP BY priority
ORDER BY
    CASE priority
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
        ELSE 5
    END;


-- ============================================================
-- 14. Strategic Alignment Portfolio Summary
-- ============================================================

SELECT
    strategic_alignment,
    COUNT(*) AS total_projects,
    SUM(CASE WHEN priority = 'Critical' THEN 1 ELSE 0 END) AS critical_projects,
    SUM(CASE WHEN priority = 'High' THEN 1 ELSE 0 END) AS high_priority_projects,
    SUM(CASE WHEN requires_executive_attention = 1 THEN 1 ELSE 0 END) AS projects_requiring_attention,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND(SUM(actual_cost), 2) AS total_actual_cost,
    ROUND(AVG(completion_percentage), 2) AS average_completion_percentage
FROM project_portfolio_enriched
GROUP BY strategic_alignment
ORDER BY
    CASE strategic_alignment
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
        ELSE 4
    END;


-- ============================================================
-- 15. Data Quality Validation: Orphan Records
-- ============================================================

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


-- ============================================================
-- 16. Data Quality Validation: Required Fields
-- ============================================================

SELECT
    COUNT(*) AS projects_missing_required_fields
FROM project_master
WHERE
    project_id IS NULL
    OR project_name IS NULL
    OR department IS NULL
    OR project_manager IS NULL
    OR status IS NULL
    OR planned_end_date IS NULL;


-- ============================================================
-- End of SQL Portfolio Analysis Queries
-- ============================================================
