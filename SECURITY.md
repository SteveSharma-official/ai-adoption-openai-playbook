# Security Policy

## Synthetic data only
This repository must never contain real tenant exports, personal information, credentials, tokens or customer data. Tallowood Advisory Group is fictional. Never commit an OpenAI API key, admin key or Compliance API token.

## Intentionally insecure material
Files under `lab-changes/` marked INTENTIONALLY INSECURE exist to be detected by the lab. Lab 0.1 contains a fake, non-working key-shaped string so the
secret check has something to find. Do not copy any of this material into a real environment.

## Optional API and workspace paths
Lab 5.2 includes an optional OpenAI API step; Labs 1.1, 6.1 and 7.2 include optional ChatGPT workspace steps. Use a dedicated sandbox API project or a
test workspace or group you are authorised to change, follow docs/openai-sandbox-setup.md and docs/cost-and-cleanup.md, and keep keys in environment
variables or a secrets manager. Never use a key from the default project or a key with all permissions.

## Reporting a vulnerability
Report suspected vulnerabilities in the lab code privately through GitHub's private vulnerability reporting for this repository.
Do not open a public issue for a vulnerability.
