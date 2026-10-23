# Lab 6.1 Workspace Build Exposure Report

**Book:** Chapter 6, section "6.3 The Grounding Document Problem"
**Difficulty:** Level 4 (Secure)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key); optional API or ChatGPT workspace path below
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
An exposure report over every workspace build (GPTs, plugins and workspace agents): which knowledge files each holds, their labels, and who the build is shared with.

## Why This Matters
A knowledge file is answerable by everyone who can use the build. The restructure plan inside a link-shared GPT is a disclosure waiting for a question.

## Enterprise Scenario
Tallowood's Advisory Restructure Q&A GPT is shared by link and holds the draft restructure plan and the partner remuneration model.

## Learning Objectives
- Inventory knowledge files by label
- Match labels to sharing scope
- Remove or restrict, then prove it

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
chapter-06/lab-01-workspace-build-exposure-report/
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
python shared/scripts/start-lab.py 6.1
cd workspace/lab-6.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `shared/datasets/tallowood/workspace_builds.json` and `knowledge_files.csv`.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Remove Restricted files from broad builds and narrow link sharing. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 6.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Remediate in waves: Restricted first, then Confidential, then set review cycles (Chapter 6).
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A builder adds the staff performance ratings to the Tax Research Helper 'for context'.
```
python ../../shared/scripts/start-lab.py 6.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `restricted-content-exposed`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: remove the file.
```
python ../../shared/scripts/start-lab.py 6.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[6.1]"
```

### Optional API or ChatGPT workspace path
Optional (workspace admin, test group only): list your workspace's builds and sharing settings and compare them with the synthetic format. WORKSPACE VALIDATION REQUIRED.
Use a dedicated sandbox API project or a test ChatGPT workspace, set a project spend limit, and follow docs/cost-and-cleanup.md.

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (restricted-content-exposed) |
| After remediation | PASS |

## Evidence
Build exposure table. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Group names here are synthetic; map them to your directory groups.

## Security Considerations
Plugin reference files and workspace agent connections inherit the same problem; the check applies to all build types.

## Enterprise Application
No build with Restricted content is shared beyond its owning group.

## Production Considerations
Review builds monthly using the admin console and the Compliance API's configuration data.

## Cleanup
Delete `workspace/lab-6.1`. If you used the optional path, delete the sandbox builds and revoke any API key you created.

## Further Challenge
Add a review date to every build and fail builds that are overdue.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23) Optional path: WORKSPACE VALIDATION REQUIRED.
