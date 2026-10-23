# Lab 8.2 OWASP Agentic Threat Model

**Book:** Chapter 8, section "8.2 The OWASP ASI Threat Catalogue"
**Difficulty:** Level 4 (Secure)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A threat model that maps each OWASP Top 10 for Agentic Applications risk (ASI01 to ASI10) to named controls in your catalogue, with an owner.

## Why This Matters
A threat with no control is an accepted risk nobody accepted. A control that is not in your catalogue is a hope.

## Enterprise Scenario
Tallowood's draft threat model covers five of ten risks and cites 'the vendor's safety' as the control for rogue agents.

## Learning Objectives
- Cover ASI01 to ASI10
- Use only controls you can evidence
- Give each risk an owner

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
chapter-08/lab-02-owasp-agentic-threat-model/
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
python shared/scripts/start-lab.py 8.2
cd workspace/lab-8.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the catalogue and threats.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Complete the map. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 8.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
ASI10 (rogue agents) is not only about your agents: Chapter 8 and Lab 8.4 cover a supplier's agent touching your systems.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Someone writes 'vendor promise' as a control.
```
python ../../shared/scripts/start-lab.py 8.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unknown-control`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 8.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[8.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unknown-control) |
| After remediation | PASS |

## Evidence
Threat to control map. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Risk names follow the OWASP list published 9 December 2025; check for revisions.

## Security Considerations
Review the model at every new tool or app connection.

## Enterprise Application
The CISO owns the model; risk owners own controls.

## Production Considerations
Link each control to evidence from other labs.

## Cleanup
Delete `workspace/lab-8.2`. No cloud resources are created by the local lab.

## Further Challenge
Score likelihood and impact for each risk.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
