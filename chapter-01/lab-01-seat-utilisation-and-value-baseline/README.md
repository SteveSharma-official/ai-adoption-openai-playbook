# Lab 1.1 Seat Utilisation and Value Baseline

**Book:** Chapter 1, section "1.1 The Renewal That Forces the Question"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key); optional API or ChatGPT workspace path below
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A seat utilisation analysis from a synthetic workspace analytics export, and a renewal case that rests on measured workflows instead of message counts.

## Why This Matters
The renewal question is not 'are people using it?'. It is 'what did we get for the money?'. Message counts answer the first and fail the second.

## Enterprise Scenario
Tallowood's CFO asks what the firm got for a year of ChatGPT Enterprise. The draft renewal paper leads with 1.2 million messages and asks for 80 more seats.

## Learning Objectives
- Separate active seats from value
- Anchor the renewal case to measured workflows with baselines and owners
- Recover seats assigned to leavers

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
chapter-01/lab-01-seat-utilisation-and-value-baseline/
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
python shared/scripts/start-lab.py 1.1
cd workspace/lab-1.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Inspect `shared/datasets/tallowood/workspace_usage.csv` (illustrative format, not OpenAI's schema). Read the renewal case.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Rewrite the renewal case around measured workflows and release leavers' seats. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 1.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Usage exports identify people. Aggregate before sharing beyond the programme team.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Someone adds 'General productivity' as a measured workflow with no baseline or owner.
```
python ../../shared/scripts/start-lab.py 1.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `workflow-without-baseline`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: remove it, or give it a baseline and an owner.
```
python ../../shared/scripts/start-lab.py 1.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[1.1]"
```

### Optional API or ChatGPT workspace path
Optional (workspace admin): export user analytics from your own workspace, map the columns to the synthetic format and re-run. WORKSPACE VALIDATION REQUIRED.
Use a dedicated sandbox API project or a test ChatGPT workspace, set a project spend limit, and follow docs/cost-and-cleanup.md.

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (workflow-without-baseline) |
| After remediation | PASS |

## Evidence
Utilisation summary and the renewal case it supports. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Active is defined here as an average of four or more active days a month; set your own threshold and write it down.

## Security Considerations
Treat usage analytics as personal information.

## Enterprise Application
The renewal paper shows workflows, baselines and owners before seat counts.

## Production Considerations
Use the workspace analytics and user analytics available in your admin console; field names differ by plan and change over time (check Appendix N).

## Cleanup
Delete `workspace/lab-1.1`. If you used the optional path, delete the sandbox builds and revoke any API key you created.

## Further Challenge
Add a third workflow and estimate the measurement effort before you commit to it.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23) Optional path: WORKSPACE VALIDATION REQUIRED.
