# Terminology

These terms are used identically in the book and in this repository.

| Term | Meaning | Book chapter | Lab |
|---|---|---|---|
| AI Adoption Maturity Model | Five levels (Experiment, Controlled pilot, Operational, Scaled, Agentic enterprise), each gated by evidence | 0 | 0.2 |
| Seat Value Baseline | Active seats compared with seats in a measured workflow; activity is not value | 1 | 1.1 |
| Value Hypothesis | Business metric, measured baseline, target, system of record, owner | 1, 3 | 1.2, 3.1 |
| Enterprise AI Portfolio Map | Places each workload on a platform by where its data lives, with a written justification for exceptions | 2 | 2.1 |
| Shadow AI Discovery | Finding unsanctioned AI use from proxy, OAuth grant and expense evidence | 2 | 2.2 |
| Decision Ladder | Seats, Workspace build, API, Frontier, Host: start at the lowest rung that meets the need | 4 | 4.1 |
| Workspace build | A custom GPT, plugin or workspace agent built inside ChatGPT Enterprise or Business (Book 3 term covering all three) | 4, 6, 7 | 6.1, 6.2, 7.2 |
| Reference Architecture as Code | Five layers (identity, experience, build, data, operations); every component has identity, owner, logging and data boundary | 5 | 5.1 |
| Agent Identity | A dedicated, least-privilege identity per agent with an owner; never a shared or default-project API key | 5 | 5.1, 5.2 |
| Build Exposure Report | What each workspace build can see: sharing scope against knowledge file classification and connected apps | 6 | 6.1 |
| GPT Retirement Decision | Migrate, retire or rebuild for every custom GPT before the vendor retirement date | 6 | 6.2 |
| Human-Agent Authority Matrix | Per action: allowed, approval (with limits) or never | 7 | 7.1, 7.2 |
| Approval Gate | Execution held until a human approval exists | 7 | 7.1, 7.2 |
| Agent Register | The authoritative list of agents with owners and risk tiers | 8 | 8.1 |
| Kill Switch | Tested procedure to pause an agent and revoke its access | 8, 17 | 8.3, 17.1 |
| AI Supplier Incident Readiness | Contract and process terms for a supplier's own AI incident: notification window, named contact, evidence, audit rights | 8, 15 | 8.4, 15.2 |
| Use-Case Discovery Canvas | Scores candidate processes on volume, effort, data readiness and documented rules | 9 | 9.1 |
| Process Archaeology | Reconstructing how a process actually runs from events and interviews | 9 | 9.1 |
| Failure Paths | Designed responses for wrong, missing and conflicting answers | 10 | 10.1 |
| Day 90 Gate | Evidence-based Go, Extend or Stop decision | 11 | 11.1 |
| Evaluation Scorecard | Accuracy, fabrication rate, citation match and human loop catch rate over a standard, edge and adversarial test set | 12 | 12.1 |
| Production Readiness Gate | Every gate item backed by evidence on file and a named sign-off (series framework, not a vendor feature) | 12 | 12.3 |
| Human Authority Line | Sector form of the authority matrix: Credit (13), Clinical (14), Public (15) | 13 to 15 | 13.1, 14.1, 15.1 |
| Agentic Audit Trail | Hash-chained, tamper-evident record of agent actions and routing | 13 | 13.1 |
| Transparency Record | Public record of how AI is used in a government decision process | 15 | 15.1 |
| Residency and IRAP Scope Check | Data at rest region, inference region, IRAP report scope and the agency's own authorisation, recorded separately | 15 | 15.2 |
| AI Operating Model RACI | Accountable and responsible people for every production agent | 17 | 17.1 |
| Model Change Control | Vendor default model changes treated as changes and evaluated before reliance | 17 | 17.2 |
| Three meters | Seats, workspace credits and API tokens, each with a guardrail | 17 | 17.3 |
| Shared Platform Model | Identity pattern, gateway, logging, evaluation and knowledge file governance reused by every agent | 18 | 18.1 |
| Executive Dashboard | Business metrics, each with a system of record and owner | 18 | 18.1 |
| Evidence pack | result.json, report.md and manifest.json (SHA-256) produced by every lab | 0 | All |
| Tallowood Advisory Group (fictional) | The synthetic organisation used in every lab | 0 | All |

## Platform names current at 2026-10-23 (volatile)
The labs model capabilities, not products. These names were checked on 2026-10-23; the book's Appendix N is the living record.

| Name | Note |
|---|---|
| ChatGPT Enterprise, ChatGPT Business, ChatGPT Edu | Workspace plans; feature availability differs by plan |
| Custom GPTs to plugins | Announced 11 September 2026: migration from 22 September, new GPT creation ends 26 October 2026, retirement 11 December 2026 (deferral to 11 February 2027 on request). Custom actions do not migrate |
| Workspace agents | Announced 22 April 2026, generally available 22 May 2026, credit-based |
| OpenAI Frontier | Announced 5 February 2026; limited availability |
| Responses API (Assistants API sunset 26 August 2026) | Assistants API workloads must move to the Responses API |
| AgentKit: Agent Builder and Evals | Launched 6 October 2025; Agent Builder and Evals wind down from 30 November 2026 |
| Data residency | At rest in several regions including Australia; inference residency only in the United States, Europe and the United Arab Emirates (checked 23 October 2026) |
| Real-time Google Drive, SharePoint and Teams apps | Replaced admin-managed sync connectors on 16 October 2026 |
| OWASP Top 10 for Agentic Applications (ASI01 to ASI10) | Published 9 December 2025 |
