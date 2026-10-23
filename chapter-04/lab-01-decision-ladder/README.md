# Lab 4.1 The Decision Ladder

**Book:** Chapter 4, section "4.3 The Decision Tree"
**Difficulty:** Level 2 (Build)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A Decision Ladder record for three workloads: the minimum rung each needs (Seats, Workspace build, API, Frontier, Host), the rung chosen, and the justification when they differ.

## Why This Matters
Every rung up adds cost, ownership and attack surface. The engineering team that asks for API access before checking whether a workspace build will do is in the tool-first trap.

## Enterprise Scenario
Tallowood's platform team proposes building the policy FAQ on the API and running meeting notes as a Frontier agent.

## Learning Objectives
- Compute the minimum rung from workload facts
- Catch over-engineering
- Record the justification for any higher rung

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
chapter-04/lab-01-decision-ladder/
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
python shared/scripts/start-lab.py 4.1
cd workspace/lab-4.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the workloads.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Choose the lowest rung that works. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 4.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
A lower rung usually means fewer identities and keys to govern.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Someone proposes meeting notes as a Frontier agent.
```
python ../../shared/scripts/start-lab.py 4.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `over-engineered`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: seats are enough.
```
python ../../shared/scripts/start-lab.py 4.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[4.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (over-engineered) |
| After remediation | PASS |

## Evidence
Rung table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Choosing Frontier also raises an availability note: it had limited availability at the time of writing.

## Security Considerations
Higher rungs need the identity and logging controls in Chapters 5 and 8 before use.

## Enterprise Application
The architecture board records rung decisions.

## Production Considerations
Re-run the ladder when a workload changes: a new integration can move it up one rung.

## Cleanup
Delete `workspace/lab-4.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a workload that genuinely needs the Host rung and explain why.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
