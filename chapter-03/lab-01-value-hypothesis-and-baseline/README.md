# Lab 3.1 Value Hypothesis and Baseline

**Book:** Chapter 3, section "3.4 The Value Hypothesis: A Statement You Can Test"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A testable value hypothesis with a value category, a business metric, a measured baseline, a target, a system of record and an owner.

## Why This Matters
'Save employees time' is not a value hypothesis. It is a hope. The CFO funds a number that can be measured and disputed.

## Enterprise Scenario
Tallowood's tax practice wants budget for a second year. Its hypothesis is a sentence about productivity and a usage chart.

## Learning Objectives
- Choose a value category
- Replace activity with an outcome metric
- Anchor to a baseline and a system of record

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
chapter-03/lab-01-value-hypothesis-and-baseline/
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
```

## Steps

### Step 1. Environment Setup
From the repository root:
```
python shared/scripts/start-lab.py 3.1
cd workspace/lab-3.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the hypothesis.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Rewrite it. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 3.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Not applicable beyond data handling.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
The metric slips back to active users for the dashboard.
```
python ../../shared/scripts/start-lab.py 3.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `vanity-metric`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 3.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[3.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (vanity-metric) |
| After remediation | PASS |

## Evidence
The hypothesis record. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Seats, messages, logins and sessions are activity metrics.

## Security Considerations
Timesheet data is personal information; aggregate it.

## Enterprise Application
Finance signs the hypothesis before the pilot starts.

## Production Considerations
Track the metric in the Executive Dashboard (Lab 18.1).

## Cleanup
Delete `workspace/lab-3.1`. No cloud resources are created by the local lab.

## Further Challenge
Write a second hypothesis in the 'quality improved' category.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
