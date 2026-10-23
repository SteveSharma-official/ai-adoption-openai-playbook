# Lab 2.1 Enterprise AI Portfolio Map

**Book:** Chapter 2, section "2.3 The Enterprise AI Portfolio Map"
**Difficulty:** Level 3 (Integrate)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key)
**API key needed:** No (local path)
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
A portfolio map that places every AI workload on a platform by archetype and data gravity, and requires a written justification when it crosses the data's natural home.

## Why This Matters
OpenAI is not your whole AI strategy. A workload grounded in SharePoint is usually better served where the data and permissions already live.

## Enterprise Scenario
Tallowood's engagement search runs on ChatGPT Enterprise over a SharePoint connector while the firm also pays for Microsoft 365 Copilot.

## Learning Objectives
- Classify each workload by archetype
- Place it by data gravity
- Record a justification for every cross-estate placement

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
chapter-02/lab-01-ai-portfolio-map/
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
python shared/scripts/start-lab.py 2.1
cd workspace/lab-2.1
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read the platforms and workloads.
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Move or justify the cross-estate workload. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 2.1 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Every cross-estate connector adds a second index and a second permission model to reconcile.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A team adds a workload with an archetype that is not on the map.
```
python ../../shared/scripts/start-lab.py 2.1 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `no-archetype`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: classify it properly.
```
python ../../shared/scripts/start-lab.py 2.1 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[2.1]"
```

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (no-archetype) |
| After remediation | PASS |

## Evidence
Placement table and a Mermaid portfolio map. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- A justification is a sentence a reviewer can disagree with, not 'business preference'.

## Security Considerations
Unsanctioned platforms fail placement.

## Enterprise Application
The architecture board ratifies the map each quarter.

## Production Considerations
Keep the map in source control and review it with the Agent Register (Lab 8.1).

## Cleanup
Delete `workspace/lab-2.1`. No cloud resources are created by the local lab.

## Further Challenge
Add a workload that belongs on Gemini Enterprise or Agentforce and justify its placement.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23)
