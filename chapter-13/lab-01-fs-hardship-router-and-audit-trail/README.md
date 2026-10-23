# Lab 13.1 Financial Services Hardship Router and Agentic Audit Trail

**Book:** Chapter 13, section "13.4 The Explainability Design"
**Difficulty:** Level 6 (Govern)
**Effort:** 75 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A router that sends hardship indicators to people deterministically, an agent that prepares but never decides credit, and a hash-chained Agentic Audit Trail that detects tampering.

## Why This Matters
The regulator's question is simple: show how this decision was made, approved and monitored. An audit trail you can alter cannot answer it.

## Enterprise Scenario
A bank client of Tallowood's advisory practice is piloting an OpenAI-based customer assistant. A customer mentions losing their job while asking for a limit increase; in the pilot, the agent approved it.

## Learning Objectives
- Route hardship deterministically, not by model judgement
- Keep credit decisions human
- Prove the audit trail is tamper-evident

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
chapter-13/lab-01-fs-hardship-router-and-audit-trail/
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
python shared/scripts/start-lab.py 13.1
cd workspace/lab-13.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the agent, router and cases.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Enable the router and remove credit actions. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 13.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Store the trail in write-once storage; the hash chain detects edits, storage prevents them.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Someone edits a record to hide a routing decision.
```
python ../../shared/scripts/start-lab.py 13.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `audit-chain-broken`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again (in reality: restore from immutable storage and investigate).
```
python ../../shared/scripts/start-lab.py 13.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[13.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (audit-chain-broken) |
| After remediation | PASS |

## Evidence
`agentic-audit-trail.jsonl` with prev/hash fields. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Any change to any record breaks every later hash.

## Security Considerations
Record the pinned model version in every record.

## Enterprise Application
Map to APRA CPS 230 and CPS 234 obligations; verify current standards.

## Production Considerations
Sign the chain head daily and store it separately.

## Cleanup
Delete `workspace/lab-13.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a reviewer field and a decision timestamp.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
