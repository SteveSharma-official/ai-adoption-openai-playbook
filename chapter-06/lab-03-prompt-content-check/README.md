# Lab 6.3 Prompt Content Check on a Compliance Export

**Book:** Chapter 6, section "6.4 The Prompt Content Problem"
**Difficulty:** Level 4 (Secure)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A scan of a synthetic Compliance API message export for tax file numbers, card numbers and Medicare numbers, with rules, retention and an export destination.

## Why This Matters
Users paste what is in front of them. The prompt surface is controlled by guidance, retention and detection through the Compliance API, not by hoping.

## Enterprise Scenario
Tallowood's export shows a client TFN, a card number and an employee's Medicare number pasted into prompts in one week.

## Learning Objectives
- Detect sensitive identifiers in prompts
- Choose block, redact or alert per pattern
- Set retention and an export destination

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
chapter-06/lab-03-prompt-content-check/
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
python shared/scripts/start-lab.py 6.3
cd workspace/lab-6.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `shared/datasets/tallowood/compliance_messages.jsonl` (synthetic; illustrative format). The identifiers are published test values.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Add rules, retention and export. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 6.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Workspace retention is set by admins; detection runs in a third-party tool fed by the Compliance API.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Retention is cleared during a settings migration.
```
python ../../shared/scripts/start-lab.py 6.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `retention-unset`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 6.3 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (retention-unset) |
| After remediation | PASS |

## Evidence
Scan results and rules. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Pattern matching gives false positives; tune it, do not switch it off.

## Security Considerations
The export itself is sensitive; protect the destination.

## Enterprise Application
The CISO signs the pattern list and the retention period.

## Production Considerations
Confirm which DLP and eDiscovery partners integrate with the Compliance API for your plan.

## Cleanup
Delete `workspace/lab-6.3`. No cloud resources are created by the local lab.

## Further Challenge
Add a pattern for Australian passport numbers.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
