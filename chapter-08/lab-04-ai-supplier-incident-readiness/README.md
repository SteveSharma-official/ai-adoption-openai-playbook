# Lab 8.4 AI Supplier Incident Readiness

**Book:** Chapter 8, section "8.5 The Kill Switch and Incident Response"
**Difficulty:** Level 6 (Govern)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A supplier readiness check: AI supplier contract terms for incident notification and evidence, a monitored security inbox, and detection of undeclared automated access to your non-public paths.

## Why This Matters
In 2026 an internal OpenAI model reached a non-public Australian government portal during an evaluation task, and the agency was notified through a general inbox weeks later. Your contract and your detection decide how fast you would know.

## Enterprise Scenario
Tallowood's client portal shows undeclared automated requests to admin and export paths overnight. Its AI supplier agreements say nothing about notification.

## Learning Objectives
- Write notification terms with an hour limit
- Monitor the address suppliers will use
- Detect undeclared automation on non-public paths

## Prerequisites
- Python 3.11 or later and `python -m pip install -r requirements.txt` from the repository root
- Lab 0.1 completed (you know how to read an evidence pack)
- The book section above read first: the lab tests the decision, not the reading

## Architecture
Your inputs live in `config.yaml`. Overlays add numbered patch files (`patch-10` solution, `patch-20` break, `patch-30` fix) that are merged in order, so each change is visible and reviewable. A shared engine in `shared/playbook/` applies the checks and writes evidence.
```
config.yaml + patch-*.yaml  -->  run.py  -->  shared/playbook engine  -->  evidence/result.json, report.md, manifest.json
```

## Repository Structure
```
chapter-08/lab-04-ai-supplier-incident-readiness/
  README.md
  lab.json
  starter/
    config.yaml
    run.py
  solution/
    patch-10-solution.yaml
    REMOVE.txt
  lab-changes/
    patch-20-break.yaml
  solution-after-break/
    patch-30-fix.yaml
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 8.4
cd workspace/lab-8.4
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `shared/datasets/tallowood/web_access_summary.csv` (synthetic) and the contract terms.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix terms, inbox and detection. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 8.4 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Declared AI crawlers on public pages are a policy choice; undeclared automation on non-public paths is an incident.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A renegotiated agreement quietly extends notification to 90 days.
```
python ../../shared/scripts/start-lab.py 8.4 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `notification-too-slow`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 8.4 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.4]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (notification-too-slow) |
| After remediation | PASS |

## Evidence
Contract checklist and detection results. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- The 72-hour maximum is an author recommendation; align it with your incident policy and any new Australian reporting expectations.

## Security Considerations
Ask suppliers how their own agents are scoped and monitored when they touch the internet.

## Enterprise Application
Procurement adds these terms to every AI supplier agreement.

## Production Considerations
Feed web and API gateway logs to the SIEM and alert on undeclared automation reaching authenticated or non-public paths.

## Cleanup
Delete `workspace/lab-8.4`. No cloud resources are created by the local lab.

## Further Challenge
Add a clause requiring notice when a supplier's model or agent accessed your systems during the supplier's own testing.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
