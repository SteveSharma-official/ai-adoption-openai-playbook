# Lab 5.2 Identity Model and API Key Audit

**Book:** Chapter 5, section "5.4 Whose Identity Is the AI Using?"
**Difficulty:** Level 4 (Secure)
**Effort:** 60 minutes
**Execution paths:** Local (default, synthetic data, no API key); optional API or ChatGPT workspace path below
**API key needed:** No (local path); the optional cloud path uses `OPENAI_API_KEY` from the environment
**Data:** synthetic only (Tallowood Advisory Group is fictional; domain tallowood.example)

## What You Will Build
An identity model for every OpenAI component (user, builder, key, service account, agent) and an audit of a synthetic API key inventory: shared keys, all-permission keys, keys in code and keys owned by leavers.

## Why This Matters
An API key is an identity with no face. One key shared by three teams means nobody can say who acted, and the person who created it left in June.

## Enterprise Scenario
Tallowood's default-project key has all permissions, is used by three teams, is stored in a config repository and belongs to a leaver.

## Learning Objectives
- Map the identity type for every component
- Find shared, over-scoped and leaver-owned keys
- Replace one shared key with one restricted key per workload

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
chapter-05/lab-02-identity-model-and-api-key-audit/
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
python shared/scripts/start-lab.py 5.2
cd workspace/lab-5.2
```
This copies `starter/` into a workspace folder that git ignores, so you can break things freely.

### Step 2. Configure
Read `shared/datasets/tallowood/api_keys.json` (synthetic; no real keys).
```
python run.py
```
Expected: `FAIL`. That failure is the finding you will fix.

### Step 3. Build
Revoke the shared key and issue scoped replacements. Compare with `solution/`.
```
python ../../shared/scripts/start-lab.py 5.2 --apply solution
```

### Step 4. Test
```
python run.py
```
Expected: `PASS`. Open `evidence/report.md` and `evidence/result.json`.

### Step 5. Secure
Restricted, project-scoped keys and service accounts limit the blast radius; keep them in a secrets manager.
Confirm `evidence/manifest.json` lists a SHA-256 hash for every evidence file.

### Step 6. Break It Safely
A developer copies a project key into a configuration repository 'for the build pipeline'.
```
python ../../shared/scripts/start-lab.py 5.2 --apply lab-changes
```
Anything marked INTENTIONALLY INSECURE is for lab use only.

### Step 7. Observe
```
python run.py
```
Expected: `FAIL` with a blocking finding `key-in-code`. Read the message: it names what changed and why it matters.

### Step 8. Remediate
Apply `solution-after-break/`: move it back to the secrets manager and rotate it.
```
python ../../shared/scripts/start-lab.py 5.2 --apply solution-after-break
```

### Step 9. Validate
```
python run.py
```
Expected: `PASS`. Prove the whole sequence from the repository root:
```
python -m pytest -q "tests/test_lab_sequences.py::test_lab_sequence[5.2]"
```

### Optional API or ChatGPT workspace path
Optional (API path): in a sandbox organisation, create a project with a restricted key, call one endpoint, then revoke the key and confirm the call fails. API VALIDATION REQUIRED.
Use a dedicated sandbox API project or a test ChatGPT workspace, set a project spend limit, and follow docs/cost-and-cleanup.md.

## Expected Results
| Stage | Expected status |
|---|---|
| Starter | FAIL |
| After your build or the solution | PASS |
| After lab-changes (break it safely) | FAIL (key-in-code) |
| After remediation | PASS |

## Evidence
Key inventory and findings. Keep the whole `evidence/` folder: the manifest lets a reviewer confirm nothing was edited after the run.

## Common Problems
- Key age is a note, not a failure; rotation policy is yours to set.

## Security Considerations
A key found in a repository is compromised: rotate it, then find out who used it.

## Enterprise Application
Every key has an owner in the Agent Register (Lab 8.1).

## Production Considerations
Use the admin API or console in a sandbox to list projects, keys and service accounts; names and fields change (check Appendix N).

## Cleanup
Delete `workspace/lab-5.2`. If you used the optional path, delete the sandbox builds and revoke any API key you created.

## Further Challenge
Add tenant-wide SCIM deprovisioning to the leaver process and test it.

---
Validation status: LOCAL VALIDATION PASSED (pytest, 2026-10-23) Optional path: API VALIDATION REQUIRED.
