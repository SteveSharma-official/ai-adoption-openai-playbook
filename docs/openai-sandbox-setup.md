# Optional OpenAI API and ChatGPT Workspace Sandbox Setup

The local path is complete on its own. Use this only for the optional steps in Labs 1.1, 5.2, 6.1 and 7.2.

## OpenAI API (Lab 5.2)
1. Create a new API project used only for these labs. Never use the default project.
2. Set a project spend limit and usage alerts before you create a key.
3. Create a restricted project key with only the permissions the lab names. Store it in the `OPENAI_API_KEY` environment variable. Never write it to a file in this repository.
4. Confirm current endpoint names in OpenAI's documentation. The Assistants API was sunset on 26 August 2026; use the Responses API.
5. Revoke the key at the end of the lab and confirm a call with it fails.
6. Record what you did and the result in the lab's `evidence/api-notes.md`.

## ChatGPT workspace (Labs 1.1, 6.1 and 7.2)
1. Use a test workspace, or a test group with test users and test files only. Workspace agents need ChatGPT Business, Enterprise or Edu.
2. List every admin setting you change and how to reverse it before you change it.
3. For Lab 7.2, turn on approval for at least one sensitive action and turn off publishing with personal credentials.
4. Never connect a real SharePoint, Google Drive or mailbox to a lab build.

Status of every optional step: API VALIDATION REQUIRED or WORKSPACE VALIDATION REQUIRED.
