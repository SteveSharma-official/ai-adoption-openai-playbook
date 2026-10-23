# Lab 12.1 Evaluation Harness

**Book:** Chapter 12, section "12.2 The Evaluation Scorecard"
**Difficulty:** Level 5 (Evaluate)
**Effort:** 90 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
An evaluation harness over 50 cases (30 standard, 10 edge, 10 adversarial) that scores accuracy, fabrication rate, citation match and the human loop's catch rate, compares with the last release and fails on regression.

## Why This Matters
The demo used twelve hand-picked questions. An evaluation set is how you know the agent works on the questions you did not pick, and the catch rate tells you whether the wrong answers are stopped.

## Enterprise Scenario
Tallowood's engagement letter assistant scores 86 per cent on the full set, fabricates a clause twice, and two wrong answers slip past the reviewer.

## Learning Objectives
- Build a test set with standard, edge and adversarial cases
- Score four metrics, including fabrication and catch rate
- Fail a release on regression

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
chapter-12/lab-01-evaluation-harness/
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
python shared/scripts/start-lab.py 12.1
cd workspace/lab-12.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the test set, thresholds and graded responses.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix the failing behaviour (here, the graded responses). Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 12.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Thresholds are author recommendations for a medium-risk advisory workflow, not industry standards. Set them by risk tier.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A prompt change drops accuracy from 94 to 90 per cent.
```
python ../../shared/scripts/start-lab.py 12.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `regression`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again (in reality: roll back the change).
```
python ../../shared/scripts/start-lab.py 12.1 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[12.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (regression) |
| After remediation | PASS |

## Evidence
`scores.json` and the scorecard. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A missing citation is not automatically a fabrication; review each failure.

## Security Considerations
Keep evaluation data synthetic or de-identified.

## Enterprise Application
No release without a scorecard.

## Production Considerations
Run the harness in CI on every prompt, tool or model change (Lab 17.2). OpenAI's hosted Evals product is being wound down from 30 November 2026; keep the harness in your own pipeline (check Appendix N).

## Cleanup
Delete `workspace/lab-12.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a freshness metric for superseded templates.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
