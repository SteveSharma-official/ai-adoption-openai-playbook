# Lab 17.3 FinOps: Seats, Credits and Tokens

**Book:** Chapter 17, section "17.5 The Lifecycle: Build to Retire"
**Difficulty:** Level 7 (Deploy)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
Unit economics for each agent across the three meters OpenAI customers pay (seats, workspace credits, API tokens), with spend guardrails and seat utilisation.

## Why This Matters
Seats are a fixed cost; credits and tokens are consumption. A consumption-priced agent can quietly cost more than the value it creates.

## Enterprise Scenario
Tallowood's proposal drafting service makes eight calls per draft and costs more than it returns.

## Learning Objectives
- Compute cost per outcome per meter
- Set project spend limits and credit alerts
- Track idle seats

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
chapter-17/lab-03-finops-seats-credits-tokens/
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
python shared/scripts/start-lab.py 17.3
cd workspace/lab-17.3
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read agents and guardrails. All prices are illustrative, not OpenAI list prices.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Add guardrails and fix the proposal service's economics. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 17.3 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Spend limits can stop a runaway agent loop; treat them as a safety control too.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Credit alerts are deleted during a workspace settings clean-up.
```
python ../../shared/scripts/start-lab.py 17.3 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `no-spend-guardrail`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution/` again.
```
python ../../shared/scripts/start-lab.py 17.3 --apply solution
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[17.3]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (no-spend-guardrail) |
| After remediation | PASS |

## Evidence
Unit economics table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Idle seats are a note, not a failure.

## Security Considerations
Not applicable beyond normal billing access control.

## Enterprise Application
Finance owns the value figures; the platform team owns cost.

## Production Considerations
Use the usage and billing exports your plan provides; workspace agent pricing moved to credits in 2026 (check Appendix N).

## Cleanup
Delete `workspace/lab-17.3`. No cloud resources are created by the local lab.

## Further Challenge
Add a per-user daily run cap.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
