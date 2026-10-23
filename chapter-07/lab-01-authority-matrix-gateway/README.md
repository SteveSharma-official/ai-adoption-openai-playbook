# Lab 7.1 Human-Agent Authority Matrix Gateway

**Book:** Chapter 7, section "7.4 Tool Calling and the Authority Boundary"
**Difficulty:** Level 4 (Secure)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A tool gateway that enforces the Human-Agent Authority Matrix: allowed actions run, approval actions wait for a human, never actions are denied, and the agent cannot reach systems directly.

## Why This Matters
When the assistant starts acting, the question changes from 'is the answer right?' to 'who allowed that?'. The gateway is where the answer is enforced.

## Enterprise Scenario
Tallowood's proposed procurement agent can create purchase orders. In the demo it also called the payment API directly.

## Learning Objectives
- Encode allowed, approval and never actions
- Route every call through the gateway
- Prove a direct call is rejected

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
chapter-07/lab-01-authority-matrix-gateway/
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
python shared/scripts/start-lab.py 7.1
cd workspace/lab-7.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the matrix and requests.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Turn on gateway-only routing. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 7.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
The agent's identity (Lab 5.2) has network access to the gateway only.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A developer wires the payment API straight to the agent for a demo.
```
python ../../shared/scripts/start-lab.py 7.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `gateway-bypass`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 7.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[7.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (gateway-bypass) |
| After remediation | PASS |

## Evidence
Decision table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Approval limits are illustrative; set your own with Finance.

## Security Considerations
Never actions stay never at every approval level.

## Enterprise Application
The CFO and CRO sign the matrix.

## Production Considerations
Implement the gateway as an MCP server or API proxy in front of every tool; workspace agents use the platform's approval settings (Lab 7.2).

## Cleanup
Delete `workspace/lab-7.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a daily cap on total agent-created purchase orders.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
