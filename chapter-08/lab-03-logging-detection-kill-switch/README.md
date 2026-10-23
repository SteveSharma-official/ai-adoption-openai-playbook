# Lab 8.3 Logging, Detection and the Kill Switch

**Book:** Chapter 8, section "8.5 The Kill Switch and Incident Response"
**Difficulty:** Level 7 (Deploy)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
Detection rules over synthetic audit and Compliance API events (an agent emailing without approval, a token spike, an all-permission key created, the export to the SIEM switched off), retention outside the platform, and a drilled kill switch.

## Why This Matters
Controls you cannot see are controls you cannot prove. The most important alert is the one that fires when someone turns off your visibility.

## Enterprise Scenario
On one night at Tallowood an agent emails a client unapproved, a shared key burns 9.4 million tokens, a new all-permission key appears and the SIEM export is paused.

## Learning Objectives
- Write detections for four agent events
- Keep logs for 365 days outside the platform
- Drill the kill switch

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
chapter-08/lab-03-logging-detection-kill-switch/
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
python shared/scripts/start-lab.py 8.3
cd workspace/lab-8.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `shared/datasets/tallowood/audit_events.jsonl` (synthetic; illustrative field names).
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Add rules, retention and drill steps. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 8.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
The export-disabled rule protects every other rule.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
An analyst deletes the export-disabled rule as 'noisy'.
```
python ../../shared/scripts/start-lab.py 8.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `undetected-event`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 8.3 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (undetected-event) |
| After remediation | PASS |

## Evidence
Alerts and kill switch record. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Every non-routine event must raise an alert.

## Security Considerations
Log content can include prompts; protect the SIEM index.

## Enterprise Application
Detections feed the security operations runbook.

## Production Considerations
Confirm which events your plan exposes through the Compliance API and audit log; coverage changes often (Appendix N).

## Cleanup
Delete `workspace/lab-8.3`. No cloud resources are created by the local lab.

## Further Challenge
Add a detection for an agent configuration change outside a change window.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
