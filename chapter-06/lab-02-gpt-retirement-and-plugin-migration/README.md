# Lab 6.2 GPT Retirement and Plugin Migration Register

**Book:** Chapter 6, section "6.5 The API Transmission Surface and the Remediation Sequence"
**Difficulty:** Level 6 (Govern)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A migration register for every custom GPT: a decision (plugin, workspace agent or retire), an active owner, a target date before retirement, and a plan for custom actions, which do not migrate.

## Why This Matters
OpenAI announced that custom GPTs will be retired and migrated to plugins. A GPT with no owner, or a custom action nobody rebuilds, stops working on a date someone else chose.

## Enterprise Scenario
Tallowood has four GPTs. One belongs to a leaver, two call custom actions, and nobody has looked at the retirement notice.

## Learning Objectives
- Decide the future of every GPT
- Find orphaned GPTs before the deadline
- Plan the custom actions that will not migrate

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
chapter-06/lab-02-gpt-retirement-and-plugin-migration/
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
python shared/scripts/start-lab.py 6.2
cd workspace/lab-6.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the register and the retirement date (from OpenAI's notice for affected Enterprise workspaces; confirm your workspace's date).
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Complete the register. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 6.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Migration resets sharing to private; re-share deliberately after the exposure check (Lab 6.1).
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
The proposal writer's action plan is cleared during a reorganisation of the register.
```
python ../../shared/scripts/start-lab.py 6.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `custom-actions-unplanned`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 6.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.2]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (custom-actions-unplanned) |
| After remediation | PASS |

## Evidence
Migration register. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Only the GPT's creator, a workspace owner or an admin can migrate it.

## Security Considerations
Rebuilt actions get the same review as any new tool (Lab 7.1).

## Enterprise Application
The register is a programme risk item until the last GPT is closed.

## Production Considerations
Dates and mechanics are volatile; check the workspace notice and Appendix N before relying on them.

## Cleanup
Delete `workspace/lab-6.2`. No cloud resources are created by the local lab.

## Further Challenge
Add a test plan for each migrated plugin.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
