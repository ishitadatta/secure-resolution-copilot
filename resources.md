# Deep Resource Scan (ServiceNow + Moveworks + Enterprise AI + Cybersecurity)

This list is intentionally focused on official documentation, standards organizations, or primary project sources.

## Platform docs
- ServiceNow Developer Portal: https://developer.servicenow.com/
- ServiceNow API Reference (Zurich): https://www.servicenow.com/docs/bundle/zurich-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html
- ServiceNow ITSM Product Docs: https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/itsm/homepage/itsm-home.html
- Moveworks Docs Hub: https://help.moveworks.com/docs
- Moveworks Developer Docs: https://help.moveworks.com/docs/developer-docs

## Security and IR standards
- NIST CSF 2.0: https://www.nist.gov/cyberframework
- NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide): https://csrc.nist.gov/pubs/sp/800/61/r2/final
- CISA KEV Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- MITRE ATT&CK: https://attack.mitre.org/
- STIX 2.1 Specification (OASIS): https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/

## Open-source implementation building blocks
- FastAPI docs: https://fastapi.tiangolo.com/
- PostgreSQL docs: https://www.postgresql.org/docs/
- Redis docs: https://redis.io/docs/latest/
- OpenSearch docs: https://docs.opensearch.org/latest/
- TheHive docs: https://docs.strangebee.com/thehive/
- Cortex docs: https://docs.strangebee.com/cortex/
- Shuffle SOAR docs: https://shuffler.io/docs
- Wazuh docs: https://documentation.wazuh.com/current/index.html

## Datasets and cyber intelligence feeds
- CIC-IDS2017 Dataset (UNB): https://www.unb.ca/cic/datasets/ids-2017.html
- CTU-13 Dataset: https://www.stratosphereips.org/datasets-ctu13
- UNSW-NB15 Dataset: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- Enron Email Dataset (CMU): https://www.cs.cmu.edu/~enron/
- PhishTank: https://phishtank.org/
- MISP Threat Sharing Platform: https://www.misp-project.org/

## Evaluation references
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- Microsoft Prompt Shields guidance: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection
- OpenAI Evals framework: https://github.com/openai/evals

## Suggested use in this repo
- Standards -> map controls and guardrails in `docs/architecture.md`.
- Datasets -> generate synthetic scenario variants in `evals/scenarios.json`.
- Platform docs -> replace mock connectors with real API integrations.
