# Lab 17.2 Model and Agent Change Control

**Book:** Chapter 17, section "17.4 The Support and Change Model"
**Difficulty:** Level 7 (Deploy)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A change log for prompts, apps, tools and models in which a vendor's default model change is treated like any other change: evaluated before the agent relies on it.

## Why This Matters
On a SaaS platform the model can change under you. New default models roll out to enterprise workspaces, sometimes on by default. Your last evaluation was for the old one.

## Enterprise Scenario
Tallowood's workspace received a new default model on a Tuesday. The engagement letter assistant used it on Wednesday with no regression run.

## Learning Objectives
- Log vendor-initiated changes as changes
- Gate reliance on a passing evaluation (Lab 12.1)
- Approve new app and tool connections

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
chapter-17/lab-02-model-and-agent-change-control/
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
python shared/scripts/start-lab.py 17.2
cd workspace/lab-17.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the change log.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix CHG-202. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 17.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Where admins can delay or control model access, use that control for production agents.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A vendor default model change lands with no evaluation.
```
python ../../shared/scripts/start-lab.py 17.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `vendor-model-change-unevaluated`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: evaluate, then accept.
```
python ../../shared/scripts/start-lab.py 17.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[17.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (vendor-model-change-unevaluated) |
| After remediation | PASS |

## Evidence
Change table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Model names here are placeholders; record the exact identifiers your platform shows.

## Security Considerations
Model and feature retirements are scheduled by the vendor; track them in Appendix N.

## Enterprise Application
Agent changes go through the same change board as other production changes, with evaluation evidence attached.

## Production Considerations
Run Lab 12.1 in CI as the gate.

## Cleanup
Delete `workspace/lab-17.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a knowledge file change type.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
