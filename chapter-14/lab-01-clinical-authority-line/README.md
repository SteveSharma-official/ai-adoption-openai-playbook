# Lab 14.1 Clinical Authority Line

**Book:** Chapter 14, section "14.1 The Clinical Authority Line"
**Difficulty:** Level 6 (Govern)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A Clinical Authority Line for discharge summaries: medication changes routed to the prescribing clinician, no patient data in grounding files, nothing released unsigned, and an output allowlist that keeps the agent drafting.

## Why This Matters
The discharge summary is better written than ever. The clinician still carries the liability, so the clinician still signs.

## Enterprise Scenario
A hospital pilot drafted a discharge summary that changed a medication and kept a patient's record in the build's knowledge files.

## Learning Objectives
- Route medication changes to a clinician
- Keep identifiable patient data out of grounding
- Prove no clinical decision is made by the agent

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
chapter-14/lab-01-clinical-authority-line/
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
python shared/scripts/start-lab.py 14.1
cd workspace/lab-14.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read drafts, router and outputs (synthetic patients).
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix routing, grounding and outputs. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 14.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Never use real patient data in a lab.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A configuration change lets the agent suggest medication changes.
```
python ../../shared/scripts/start-lab.py 14.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `clinical-decision-by-agent`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 14.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[14.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (clinical-decision-by-agent) |
| After remediation | PASS |

## Evidence
Draft review and output review. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- This is a governance model, not clinical guidance.

## Security Considerations
Health information is sensitive information under the Privacy Act and state health records laws.

## Enterprise Application
The CMO signs the Clinical Authority Line.

## Production Considerations
Check whether any function is software as a medical device under current TGA rules before go-live.

## Cleanup
Delete `workspace/lab-14.1`. No cloud resources are created by the local lab.

## Further Challenge
Add an allergy reconciliation check.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
