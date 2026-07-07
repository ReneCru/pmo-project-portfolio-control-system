cat > docs/risk_scoring_model.md <<'EOF'
# Risk Scoring Model: PMO Project Portfolio Control System

## 1. Purpose

This document defines the risk scoring model used in the PMO Project Portfolio Control System.

The purpose of the model is to provide a standardized method for evaluating, comparing, and prioritizing project risks across the portfolio.

The model helps the PMO and leadership team identify which projects require attention based on risk probability, business impact, and overall exposure.

---

## 2. Risk Management Context

In a project portfolio environment, risks may affect schedule, budget, quality, resources, compliance, stakeholder alignment, or business continuity.

Without a standard scoring model, risk evaluation becomes subjective. One project manager may classify a risk as critical, while another may classify a similar risk as moderate.

This scoring model creates consistency across the portfolio by assigning numeric values to probability and impact.

---

## 3. Risk Score Formula

The model uses the following formula:

Risk Score = Probability × Impact

Where:

| Component | Description |
|---|---|
| Probability | Likelihood that the risk will occur |
| Impact | Severity of the effect if the risk occurs |
| Risk Score | Combined risk exposure value |

The minimum possible score is 1.

The maximum possible score is 25.

---

## 4. Probability Scale

Probability measures how likely it is that a risk will occur.

| Score | Level | Description |
|---|---|---|
| 1 | Very Low | Risk is unlikely to occur |
| 2 | Low | Risk may occur, but probability is limited |
| 3 | Medium | Risk has a reasonable chance of occurring |
| 4 | High | Risk is likely to occur |
| 5 | Very High | Risk is expected to occur or is already emerging |

---

## 5. Impact Scale

Impact measures the severity of the consequence if the risk occurs.

| Score | Level | Description |
|---|---|---|
| 1 | Very Low | Minimal impact on project performance |
| 2 | Low | Minor impact on schedule, budget, or scope |
| 3 | Medium | Moderate impact requiring management attention |
| 4 | High | Significant impact on project delivery or cost |
| 5 | Very High | Critical impact on business objectives, delivery, or compliance |

---

## 6. Risk Score Classification

The risk score is classified into three levels.

| Risk Score Range | Risk Level | Interpretation |
|---|---|---|
| 1 - 5 | Low Risk | Monitor as part of normal project tracking |
| 6 - 14 | Medium Risk | Requires mitigation planning and PMO visibility |
| 15 - 25 | High Risk | Requires immediate attention or executive escalation |

---

## 7. Risk Matrix

The following matrix shows how probability and impact combine to create the risk score.

| Probability \ Impact | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 5 | 5 | 10 | 15 | 20 | 25 |
| 4 | 4 | 8 | 12 | 16 | 20 |
| 3 | 3 | 6 | 9 | 12 | 15 |
| 2 | 2 | 4 | 6 | 8 | 10 |
| 1 | 1 | 2 | 3 | 4 | 5 |

---

## 8. Risk Categories

The system will classify project risks using the following categories:

| Risk Category | Description |
|---|---|
| Schedule | Risks related to deadlines, delays, dependencies, or delivery dates |
| Budget | Risks related to cost overruns, funding gaps, or inaccurate estimates |
| Resource | Risks related to staffing, workload, skills, or availability |
| Scope | Risks related to unclear requirements, scope creep, or changing priorities |
| Quality | Risks related to defects, rework, testing issues, or poor deliverables |
| Compliance | Risks related to regulatory, audit, contractual, or internal control requirements |
| Stakeholder | Risks related to sponsor alignment, communication, or decision delays |
| Technology | Risks related to systems, tools, integrations, data, or infrastructure |
| Supplier | Risks related to external vendors, materials, lead times, or service providers |
| Operational | Risks related to process disruption, production impact, or business continuity |

---

## 9. Risk Status Values

Each risk will have a status value to support tracking and reporting.

| Status | Description |
|---|---|
| Open | Risk is active and requires monitoring |
| Mitigation In Progress | Mitigation actions are being executed |
| Escalated | Risk requires leadership attention |
| Closed | Risk is no longer active |
| Accepted | Risk has been acknowledged and accepted by leadership |

---

## 10. Mitigation Priority Logic

The system will use the risk level to determine mitigation priority.

| Risk Level | Expected Action |
|---|---|
| Low Risk | Monitor during regular project reviews |
| Medium Risk | Assign owner and define mitigation plan |
| High Risk | Escalate to PMO leadership and track corrective actions |

High-risk items should be reviewed first during portfolio review meetings.

---

## 11. Executive Escalation Rules

A project risk may require executive escalation when one or more of the following conditions apply:

- Risk score is 15 or higher
- Risk status is Escalated
- Risk category is Compliance and impact is 4 or higher
- Risk category is Budget and the project is already over budget
- Risk category is Schedule and the project has overdue milestones
- Risk has no assigned owner
- Risk has no mitigation plan
- Risk remains open for an extended period

These rules help leadership focus on the risks that can materially affect the project portfolio.

---

## 12. Data Fields Required

The risk scoring model requires the following fields in the risk dataset:

| Field Name | Description |
|---|---|
| Risk ID | Unique identifier for each risk |
| Project ID | Project associated with the risk |
| Risk Category | Type of risk |
| Risk Description | Summary of the risk |
| Probability | Likelihood score from 1 to 5 |
| Impact | Impact score from 1 to 5 |
| Risk Score | Probability multiplied by Impact |
| Risk Level | Low, Medium, or High |
| Risk Owner | Person responsible for managing the risk |
| Mitigation Plan | Planned action to reduce or control the risk |
| Status | Current risk status |
| Date Identified | Date when the risk was identified |

---

## 13. Use in Python

Python will be used to calculate the risk score and classify the risk level.

Expected logic:

Risk Score = Probability × Impact

Risk Level:
- 1 to 5 = Low Risk
- 6 to 14 = Medium Risk
- 15 to 25 = High Risk

Python will also generate portfolio-level risk summary outputs such as:

- Total open risks
- High-risk projects
- Risks by category
- Risks by department
- Portfolio risk exposure
- Projects requiring executive escalation

---

## 14. Use in SQL

SQL will be used to query and analyze risk data.

Expected SQL analysis includes:

- Count of high-risk projects
- Top risks by score
- Risks grouped by category
- Risks grouped by project manager
- Risks grouped by department
- Open risks requiring escalation
- Projects with both high risk and budget overrun
- Projects with high risk and overdue milestones

---

## 15. Use in Power BI

Power BI will use the risk scoring model to create executive visuals.

Expected dashboard components include:

- High Risk Projects KPI card
- Portfolio Risk Exposure KPI card
- Risk level distribution chart
- Risk category breakdown
- Top 10 project risks table
- Executive escalation table
- Risk heatmap using probability and impact
- Department risk exposure view

---

## 16. Limitations

This model is designed for portfolio-level reporting and prioritization.

It does not replace detailed project-level risk analysis, financial forecasting, or formal enterprise risk management processes.

The model is intentionally simple so that it can be easily explained, implemented, and visualized in Python, SQL, and Power BI.

---

## 17. Future Improvements

Future versions of this model may include:

- Weighted risk scoring
- Automated escalation rules
- Aging analysis for open risks
- Risk trend analysis over time
- Predictive risk classification
- Machine learning-based risk forecasting
- Integration with Jira, Microsoft Project, Smartsheet, or SharePoint
- Automated risk summary generation for executives

---

## 18. Summary

The risk scoring model provides a consistent method to evaluate project risks across a PMO portfolio.

By using probability, impact, risk score, and risk level classification, the system helps identify which projects require monitoring, mitigation, or executive escalation.

This model supports stronger project governance, better decision-making, and clearer portfolio visibility.
EOF