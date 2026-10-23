# Lab 15.2 Hosting, Residency and IRAP Scope Check

**Book:** Chapter 15, section "15.2 The Government Regulatory Map"
**Difficulty:** Level 6 (Govern)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A check of a synthetic agency deployment against the vendor's published residency regions, the services in scope of any IRAP report you hold, and the agency's own authorisation decision.

## Why This Matters
Data residency at rest is not inference residency, and neither is an IRAP assessment. An IRAP report informs the agency's risk-based authorisation; it does not certify a deployment.

## Enterprise Scenario
A state agency wants ChatGPT Enterprise for OFFICIAL work. Its workspace stores data in the United States, and no IRAP report covers the service.

## Learning Objectives
- Separate data at rest, inference and assessment
- Record the agency's authorisation and any risk acceptance
- Require a supplier incident notification clause

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
chapter-15/lab-02-hosting-residency-and-irap-scope-check/
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
python shared/scripts/start-lab.py 15.2
cd workspace/lab-15.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the vendor facts (from OpenAI's help centre on 23 October 2026; re-check before use) and the deployment.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Move data at rest to Australia, record the acceptance and authorisation, add the clause. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 15.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Residency options depend on plan and are typically chosen when a workspace or project is created; confirm with the vendor.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A new workload is added that requires onshore inference.
```
python ../../shared/scripts/start-lab.py 15.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `inference-offshore`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: keep that workload off the platform.
```
python ../../shared/scripts/start-lab.py 15.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[15.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (inference-offshore) |
| After remediation | PASS |

## Evidence
Deployment check. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- An empty IRAP list is a fact to record, not a failure to hide.

## Security Considerations
Classification limits and the Hosting Certification Framework apply; verify current requirements.

## Enterprise Application
The agency CISO owns the authorisation decision.

## Production Considerations
Re-run when the vendor adds regions or publishes assessments, and when the deployment changes.

## Cleanup
Delete `workspace/lab-15.2`. No cloud resources are created by the local lab.

## Further Challenge
Add key management and operator access requirements.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
