# Lab 8.1 Agent Register

**Book:** Chapter 8, section "8.1 The Control Plane: One View of the Estate"
**Difficulty:** Level 6 (Govern)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
An Agent Register reconciled against what exists across GPTs, workspace agents, API services and Frontier proposals: owner, risk tier and identity for each.

## Why This Matters
You cannot govern what you cannot list. The control plane starts with one view of every agent, wherever it was built.

## Enterprise Scenario
Tallowood's register misses the API proposal service and lists a leaver as owner of People Answers.

## Learning Objectives
- Reconcile discovered agents with the register
- Fix orphaned ownership
- Record an identity type for each agent

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
chapter-08/lab-01-agent-register/
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
python shared/scripts/start-lab.py 8.1
cd workspace/lab-8.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `agents.json` and the register.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Reconcile. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 8.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
An agent with no identity entry cannot be revoked quickly.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A new workspace agent appears that nobody registered.
```
python ../../shared/scripts/start-lab.py 8.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unregistered-agent`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 8.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unregistered-agent) |
| After remediation | PASS |

## Evidence
Reconciliation table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Discovery sources: admin console, Compliance API configuration data, API project lists, Frontier inventory if you have it.

## Security Considerations
Unregistered agents are a finding, not a paperwork gap.

## Enterprise Application
Registration is a precondition for production (Lab 12.3).

## Production Considerations
Automate discovery weekly and diff against the register.

## Cleanup
Delete `workspace/lab-8.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a last-reviewed date and fail entries older than 90 days.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
