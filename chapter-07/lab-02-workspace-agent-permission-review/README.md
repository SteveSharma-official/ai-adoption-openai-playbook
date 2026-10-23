# Lab 7.2 Workspace Agent Permission Review

**Book:** Chapter 7, section "7.5 The Approval Gate and the Never List"
**Difficulty:** Level 4 (Secure)
**Effort:** 45 minutes
**Execution paths:** Local (default, synthetic data, no API key); optional API or ChatGPT workspace path below
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A review of workspace agents against policy: no shared agent runs on its builder's personal credentials, sensitive actions require approval, and only approved apps are connected.

## Why This Matters
A shared agent on personal credentials means everyone who runs it acts as the builder. An agent that sends email without asking is acting in your name.

## Enterprise Scenario
Tallowood's Weekly Pipeline Digest is shared with Advisory, uses its builder's credentials and emails clients without approval.

## Learning Objectives
- Find shared agents on personal credentials
- Require approval for sensitive actions
- Restrict connected apps

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
chapter-07/lab-02-workspace-agent-permission-review/
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
python shared/scripts/start-lab.py 7.2
cd workspace/lab-7.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the workspace agent entries in the dataset.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Fix the digest agent. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 7.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
OpenAI recommends keeping the personal-credential publishing setting narrowly scoped; this lab makes it a policy.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
Approval for send_email is turned off on the supplier onboarding agent to 'reduce friction'.
```
python ../../shared/scripts/start-lab.py 7.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `approval-off-for-sensitive-action`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`.
```
python ../../shared/scripts/start-lab.py 7.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[7.2]"
```

### Optional API or ChatGPT workspace path
Optional (workspace admin, test group): build a workspace agent with approval on for one sensitive action, run it, and record the approval prompt. WORKSPACE VALIDATION REQUIRED.
Use a dedicated sandbox API project or a test ChatGPT workspace, set a project spend limit, and follow docs/cost-and-cleanup.md.

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (approval-off-for-sensitive-action) |
| After remediation | PASS |

## Evidence
Review table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Settings names change; map them to your admin console.

## Security Considerations
Approvals are a control only if the approver reads the action.

## Enterprise Application
Workspace agents enter the Agent Register (Lab 8.1).

## Production Considerations
Monitor agent runs and configuration changes through the Compliance API; pause agents that drift.

## Cleanup
Delete `workspace/lab-7.2`. If you used the optional path, delete the sandbox builds and revoke any API key you created.

## Further Challenge
Add a check that every shared agent has a named business owner.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23) Optional path: WORKSPACE VALIDATION REQUIRED.
