# Lab 0.2 AI Adoption Maturity Self-Assessment

**Book:** Chapter 0, section "0.3 The Question This Book Answers"
**Difficulty:** Level 1 (Explore)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A scored maturity baseline that counts only evidenced items, so the level you report is the level you can defend.

## Why This Matters
Most organisations that bought seats in a hurry rate themselves a level higher than their evidence supports. The gap is the next piece of work.

## Enterprise Scenario
Tallowood's steering group reports 'Level 3, operational'. The evidence pack shows no data boundary was ever written down.

## Learning Objectives
- Score maturity from evidence, not opinion
- Find the first gap
- Separate claimed from evidenced level

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
chapter-00/lab-02-maturity-self-assessment/
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
python shared/scripts/start-lab.py 0.2
cd workspace/lab-0.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the evidence items in `config.yaml`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Record the level the evidence supports. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 0.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Evidence entries name documents and owners, not content.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
The level is nudged up to 2 for the board paper.
```
python ../../shared/scripts/start-lab.py 0.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `maturity-overclaim`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: write the missing data boundary, and Level 2 becomes true.
```
python ../../shared/scripts/start-lab.py 0.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[0.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (maturity-overclaim) |
| After remediation | PASS |

## Evidence
Scored levels and the first gap. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A level is met only when every item at that level and below is met.

## Security Considerations
Do not paste confidential content into evidence fields.

## Enterprise Application
Re-score each quarter and report movement, not the score.

## Production Considerations
Store the assessment with the programme's governance records.

## Cleanup
Delete `workspace/lab-0.2`. No cloud resources are created by the local lab.

## Further Challenge
Add your own Level 3 evidence items for your organisation.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
