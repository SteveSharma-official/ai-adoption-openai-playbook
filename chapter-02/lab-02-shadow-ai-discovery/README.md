# Lab 2.2 Shadow AI Discovery

**Book:** Chapter 2, section "2.5 The Shared Governance Layer"
**Difficulty:** Level 4 (Secure)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A shadow AI register built from three synthetic signals (proxy summary, app consent grants and expense lines), with a decision and an owner for each.

## Why This Matters
You did not choose this adoption. Personal ChatGPT accounts, note-takers and PDF tools were in use before the enterprise workspace existed.

## Enterprise Scenario
Tallowood's proxy shows nine people still using personal ChatGPT accounts, and an expense claim shows a personal API account.

## Learning Objectives
- Combine proxy, consent and expense signals
- Decide migrate, block or review for each
- Name an owner for every review

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
chapter-02/lab-02-shadow-ai-discovery/
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
python shared/scripts/start-lab.py 2.2
cd workspace/lab-2.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the three dataset files.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Record decisions. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 2.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Blocking is the start of a conversation: offer the governed alternative.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A new app consent appears with read-write access to documents.
```
python ../../shared/scripts/start-lab.py 2.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `unreviewed-ai-signal`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: decide it.
```
python ../../shared/scripts/start-lab.py 2.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[2.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (unreviewed-ai-signal) |
| After remediation | PASS |

## Evidence
Signal register with decisions. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- An expense line counts as a signal even for one user.

## Security Considerations
Review consent grants for write and send scopes first.

## Enterprise Application
Shadow AI review becomes a monthly control.

## Production Considerations
Use your proxy, identity provider consent logs and expense system; the synthetic files show the shape, not a vendor format.

## Cleanup
Delete `workspace/lab-2.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a signal from browser extension inventory.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
