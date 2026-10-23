# Lab 5.1 Reference Architecture as Code

**Book:** Chapter 5, section "5.5 The Reference Architecture"
**Difficulty:** Level 2 (Build)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
The OpenAI reference architecture as code: five layers (workspace, workspace builds, API platform, agent platform, governance), each component with an identity, owner, logging destination and data boundary.

## Why This Matters
Every organisation with seats already has an AI architecture. Most have never drawn it, so nobody can say where the data goes or whose identity acts.

## Enterprise Scenario
Tallowood's CIO is asked to approve a Frontier agent and cannot answer where contract data goes or which identity the API integration uses.

## Learning Objectives
- Draw all five layers, even if one is empty
- Give every component an identity, owner, log destination and data boundary
- Generate a diagram from the source

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
chapter-05/lab-01-reference-architecture-as-code/
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
python shared/scripts/start-lab.py 5.1
cd workspace/lab-5.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `config.yaml`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fill the gaps. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 5.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
An empty agent platform layer is still drawn: it is where the next approval request will land.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A new contract review bot appears, authenticated with the shared key.
```
python ../../shared/scripts/start-lab.py 5.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `shared-key-identity`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: give it its own restricted service account.
```
python ../../shared/scripts/start-lab.py 5.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[5.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (shared-key-identity) |
| After remediation | PASS |

## Evidence
Component table and `reference-architecture.mmd`. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- 'logging: none' counts as present text; the check is that a destination is named. Write a real destination.

## Security Considerations
Zero data retention is available only for eligible endpoints and use cases; request it, do not assume it.

## Enterprise Application
The architecture is signed by the CIO and CISO.

## Production Considerations
Keep the source in the repository and render it in the architecture repository.

## Cleanup
Delete `workspace/lab-5.1`. No cloud resources are created by the local lab.

## Further Challenge
Add Codex and its service accounts as a sixth layer.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
