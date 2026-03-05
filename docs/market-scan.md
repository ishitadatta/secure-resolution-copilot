# Market Scan (as of March 5, 2026)

## Existing enterprise products

| Product | What it clearly does | Source |
|---|---|---|
| ServiceNow Security Incident Response | Case workflows, prioritization, remediation coordination, SecOps dashboards | https://www.servicenow.com/products/security-incident-response.html |
| ServiceNow + Moveworks (EmployeeWorks) | Conversational front door and workflow execution across systems | https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-launches-Autonomous-Workforce-that-thinks-and-acts-adds-Moveworks-to-the-ServiceNow-AI-Platform/default.aspx |
| Moveworks Data API / Embedded Assistant | Access interaction telemetry and embed assistant in web portals | https://help.moveworks.com/docs/data-api and https://help.moveworks.com/docs/moveworks-for-web |
| Splunk SOAR | Playbook orchestration, case management, broad integrations/actions | https://help.splunk.com/en/splunk-soar and https://www.splunk.com/en_us/products/splunk-security-orchestration-and-automation.html |
| Google SecOps SOAR | Alert grouping, prioritization, playbook automation, SOAR APIs/SDK | https://docs.cloud.google.com/chronicle/docs/soar |
| IBM QRadar SOAR | Dynamic playbooks, case management, orchestration and response | https://www.ibm.com/products/qradar-soar |
| Microsoft Security Copilot | AI copilots/agents for investigation and response in security workflows | https://www.microsoft.com/en-us/security/business/ai-machine-learning/microsoft-copilot-security and https://learn.microsoft.com/en-us/copilot/security/get-started-security-copilot |
| Cortex XSOAR | Visual playbooks and community content repository for SOC automation | https://xsoar.pan.dev/ and https://github.com/cohesity/cortex-xsoar |

## Gap this project now targets

Most platforms focus on automation execution at scale. This project focuses on a missing developer and operations experience:

1. One-click, end-to-end **Scenario Mission** that is reproducible on a laptop.
2. Deterministic **mission report** (triage match, actions executed, assurance checks).
3. Built-in **assurance proof** + counterfactual impact simulation.
4. Built-in **safety challenge** checks in the same flow.

This is designed as a product validation harness for enterprise AI workflows, not just a case-management mock.
