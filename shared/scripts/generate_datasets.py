#!/usr/bin/env python3
"""Generate the synthetic Tallowood Advisory Group dataset used by every lab.

Tallowood Advisory Group is fictional (domain tallowood.example). It is a mid-size Australian professional services firm
(audit, tax and advisory) with ChatGPT Enterprise seats, a set of GPTs that face retirement, API integrations built by two
teams, a Frontier pilot proposal, and a Microsoft 365 document estate. Deterministic: the same seed always produces the same files.

  python shared/scripts/generate_datasets.py
"""
import csv, json, random, datetime as dt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "datasets" / "tallowood"
R = random.Random(20261023)

FIRST = ["Ava", "Liam", "Mia", "Noah", "Isla", "Jack", "Zara", "Ethan", "Ruby", "Arjun", "Chloe", "Leo", "Priya", "Tom", "Grace",
         "Sam", "Nina", "Omar", "Ella", "Ben", "Hana", "Luca", "Maya", "Ravi", "Sofia", "Kai", "Lily", "Max", "Aria", "Dev"]
LAST = ["Nguyen", "Smith", "Patel", "Brown", "Wilson", "Chen", "Taylor", "Singh", "Martin", "Kelly", "Rossi", "Walker",
        "Khan", "Lee", "Murphy", "Hall", "Young", "King", "Wright", "Scott"]
DEPTS = [("Audit and Assurance", "VIC"), ("Finance", "VIC"), ("People", "NSW"), ("Tax", "NSW"), ("Client Services", "QLD"),
         ("Advisory", "VIC"), ("Executive", "VIC"), ("IT and Security", "VIC"), ("Procurement", "QLD"), ("Legal", "VIC")]


def w(name, rows, cols):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def j(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    users = []
    for i in range(1, 61):
        d, st = DEPTS[(i - 1) % len(DEPTS)]
        users.append({"user_id": f"u{i:03d}", "name": f"{FIRST[(i * 7) % 30]} {LAST[(i * 3) % 20]}",
                      "email": f"u{i:03d}@tallowood.example", "department": d, "state": st,
                      "role": "Graduate" if i in (12, 33) else ("Manager" if i % 10 == 1 else "Staff"),
                      "status": "leaver" if i in (27, 48) else "active"})
    w("users.csv", users, list(users[0]))
    groups = {"all-staff": [u["user_id"] for u in users],
              "people-team": [u["user_id"] for u in users if u["department"] == "People"],
              "executive": [u["user_id"] for u in users if u["department"] == "Executive"],
              "advisory": [u["user_id"] for u in users if u["department"] == "Advisory"],
              "builders": ["u006", "u016", "u026", "u008"]}
    w("group_members.csv", [{"group": g, "user_id": m} for g, ms in groups.items() for m in ms], ["group", "user_id"])

    # Lab 1.1: workspace analytics export (illustrative format, not OpenAI's exact schema)
    usage = []
    for u in users:
        if u["status"] == "leaver":
            continue
        n = int(u["user_id"][1:])
        tier = "power" if n % 7 == 0 else ("dormant" if n % 4 == 0 else "casual")
        for m in ("2026-07", "2026-08", "2026-09"):
            days = {"power": R.randint(15, 21), "casual": R.randint(2, 9), "dormant": 0}[tier]
            usage.append({"user_id": u["user_id"], "month": m, "active_days": days, "messages": days * R.randint(4, 30),
                          "in_measured_workflow": "yes" if tier == "power" and u["department"] in ("Tax", "Audit and Assurance") else "no"})
    w("workspace_usage.csv", usage, ["user_id", "month", "active_days", "messages", "in_measured_workflow"])

    # Lab 1.2: engagement letter process events (received -> conflicts -> drafted -> reviewed -> signed)
    events = []
    for c in range(1, 41):
        t = dt.datetime(2026, 7, 1, 9) + dt.timedelta(days=c, hours=R.randint(0, 6))
        for s, gap in [("received", 0), ("conflicts_checked", R.randint(8, 30)), ("drafted", R.randint(10, 40)),
                       ("partner_reviewed", R.randint(6, 30)), ("signed", R.randint(20, 70))]:
            t = t + dt.timedelta(hours=gap)
            events.append({"case_id": f"EL{c:03d}", "step": s, "ts": t.isoformat()})
    w("engagement_letter_events.csv", events, ["case_id", "step", "ts"])

    # Lab 2.2: shadow AI signals
    proxy = [{"domain": "chatgpt.com", "account_type": "enterprise", "users": 41, "uploads_mb": 380},
             {"domain": "chatgpt.com", "account_type": "personal", "users": 9, "uploads_mb": 62},
             {"domain": "notetaker-ai.example", "account_type": "personal", "users": 7, "uploads_mb": 140},
             {"domain": "pdfchat.example", "account_type": "personal", "users": 4, "uploads_mb": 35},
             {"domain": "claude.ai", "account_type": "personal", "users": 3, "uploads_mb": 12}]
    w("proxy_ai_summary.csv", proxy, list(proxy[0]))
    expenses = [{"claim": "EX1041", "user_id": "u015", "vendor": "OpenAI (ChatGPT Plus)", "amount": 32.0},
                {"claim": "EX1077", "user_id": "u025", "vendor": "OpenAI (API)", "amount": 118.4},
                {"claim": "EX1102", "user_id": "u035", "vendor": "NoteTaker AI Pro", "amount": 29.0}]
    w("expense_ai_lines.csv", expenses, list(expenses[0]))
    grants = [{"app": "ChatGPT Enterprise (sanctioned)", "scopes": "SharePoint, Outlook app", "users": 51, "sanctioned": "yes", "data_access": "documents"},
              {"app": "NoteTaker AI", "scopes": "Calendars.Read Files.Read.All", "users": 7, "sanctioned": "no", "data_access": "documents"},
              {"app": "PDF Chat", "scopes": "Files.Read", "users": 4, "sanctioned": "no", "data_access": "documents"},
              {"app": "MailMate GPT", "scopes": "Mail.Send", "users": 5, "sanctioned": "no", "data_access": "email"}]
    w("oauth_grants.csv", grants, list(grants[0]))

    # Lab 5.2: API key inventory (synthetic; never real keys)
    keys = [{"key_id": "key_a1", "project": "tax-research", "owner": "u016", "type": "project", "permissions": "restricted", "created": "2026-03-02",
             "last_used": "2026-10-21", "used_by": ["Tax"], "stored_in": "secret_manager"},
            {"key_id": "key_b7", "project": "default", "owner": "u027", "type": "user", "permissions": "all", "created": "2025-06-11",
             "last_used": "2026-10-22", "used_by": ["Advisory", "Client Services", "Procurement"], "stored_in": "config_repo"},
            {"key_id": "key_c3", "project": "proposal-drafts", "owner": "u026", "type": "project", "permissions": "restricted", "created": "2026-08-19",
             "last_used": "2026-10-20", "used_by": ["Advisory"], "stored_in": "env_var"},
            {"key_id": "sa_d9", "project": "procurement-agent", "owner": "u009", "type": "service_account", "permissions": "restricted", "created": "2026-09-30",
             "last_used": "2026-10-22", "used_by": ["Procurement"], "stored_in": "secret_manager"}]
    j("api_keys.json", keys)

    # Labs 6.1, 6.2, 7.2: workspace builds (GPTs, plugins, workspace agents)
    files = [{"file_id": "kf01", "title": "Partner Remuneration Model FY27", "label": "Restricted"},
             {"file_id": "kf02", "title": "Tax Practice Guide 2026", "label": "Internal"},
             {"file_id": "kf03", "title": "Restructure Plan Advisory (draft)", "label": "Restricted"},
             {"file_id": "kf04", "title": "Engagement Letter Templates", "label": "Internal"},
             {"file_id": "kf05", "title": "Client Fee Schedule", "label": "Confidential"},
             {"file_id": "kf06", "title": "Proposal Win Themes", "label": "Internal"},
             {"file_id": "kf07", "title": "Staff Performance Ratings 2026", "label": "Restricted"}]
    w("knowledge_files.csv", files, ["file_id", "title", "label"])
    builds = [
        {"build_id": "gpt-01", "name": "Tax Research Helper", "type": "gpt", "owner": "u016", "sharing": "group:tax", "knowledge": ["kf02"],
         "apps": [], "custom_actions": [], "personal_credentials": False, "approvals": {}},
        {"build_id": "gpt-02", "name": "People Answers", "type": "gpt", "owner": "u027", "sharing": "workspace", "knowledge": ["kf07", "kf04"],
         "apps": ["SharePoint"], "custom_actions": ["hris_lookup"], "personal_credentials": False, "approvals": {}},
        {"build_id": "gpt-03", "name": "Proposal Writer", "type": "gpt", "owner": "u026", "sharing": "workspace", "knowledge": ["kf06", "kf05"],
         "apps": [], "custom_actions": ["crm_opportunity"], "personal_credentials": False, "approvals": {}},
        {"build_id": "gpt-04", "name": "Advisory Restructure Q&A", "type": "gpt", "owner": "u006", "sharing": "link", "knowledge": ["kf03", "kf01"],
         "apps": [], "custom_actions": [], "personal_credentials": False, "approvals": {}},
        {"build_id": "plg-01", "name": "Engagement Letter Drafter", "type": "plugin", "owner": "u016", "sharing": "group:tax", "knowledge": ["kf04"],
         "apps": ["SharePoint"], "custom_actions": [], "personal_credentials": False, "approvals": {}},
        {"build_id": "wsa-01", "name": "Weekly Pipeline Digest", "type": "workspace_agent", "owner": "u026", "sharing": "group:advisory", "knowledge": [],
         "apps": ["Outlook", "SharePoint"], "custom_actions": [], "personal_credentials": True, "approvals": {"send_email": False}},
        {"build_id": "wsa-02", "name": "Supplier Onboarding Agent", "type": "workspace_agent", "owner": "u009", "sharing": "group:procurement",
         "knowledge": [], "apps": ["Outlook"], "custom_actions": [], "personal_credentials": False, "approvals": {"send_email": True}}]
    j("workspace_builds.json", builds)

    # Lab 6.3: prompt content sample from a Compliance API style export (synthetic; illustrative format)
    msgs = [{"conv": "c01", "user_id": "u014", "text": "Summarise the attached engagement terms for the client in plain English."},
            {"conv": "c02", "user_id": "u024", "text": "Client TFN is 123 456 782, can you prepare the lodgement checklist?"},
            {"conv": "c03", "user_id": "u034", "text": "Draft an email confirming the meeting on Thursday."},
            {"conv": "c04", "user_id": "u044", "text": "Refund the client to card 4111 1111 1111 1111 and draft the note."},
            {"conv": "c05", "user_id": "u054", "text": "Rewrite this paragraph to be more concise."},
            {"conv": "c06", "user_id": "u013", "text": "Employee medical certificate says Medicare 2123 45670 1, summarise the leave request."}]
    (OUT / "compliance_messages.jsonl").write_text("\n".join(json.dumps(m) for m in msgs) + "\n", encoding="utf-8")

    # Lab 8.1 and 17.1: agents discovered across surfaces
    agents = [{"agent_id": "ag-01", "name": "Tax Research Helper", "surface": "GPT", "status": "production"},
              {"agent_id": "ag-02", "name": "People Answers", "surface": "GPT", "status": "production"},
              {"agent_id": "ag-03", "name": "Weekly Pipeline Digest", "surface": "Workspace agent", "status": "pilot"},
              {"agent_id": "ag-04", "name": "Supplier Onboarding Agent", "surface": "Workspace agent", "status": "pilot"},
              {"agent_id": "ag-05", "name": "Procurement Agent", "surface": "Frontier (proposed)", "status": "proposal"},
              {"agent_id": "ag-06", "name": "Proposal Drafting Service", "surface": "API (Responses API)", "status": "production"}]
    j("agents.json", agents)

    # Lab 8.3: audit and Compliance API style events (synthetic; illustrative field names)
    ev = []
    base = dt.datetime(2026, 10, 19, 8)
    for i in range(36):
        ev.append({"ts": (base + dt.timedelta(minutes=23 * i)).isoformat(), "actor": "ag-04", "event": "agent.run", "detail": "routine"})
    ev += [{"ts": "2026-10-20T02:11:00", "actor": "ag-03", "event": "app.action", "detail": "send_email external recipient", "approval": None},
           {"ts": "2026-10-20T02:40:00", "actor": "key_b7", "event": "api.usage", "detail": "tokens", "tokens": 9_400_000},
           {"ts": "2026-10-20T09:30:00", "actor": "u027", "event": "admin.api_key.created", "detail": "user key, all permissions"},
           {"ts": "2026-10-21T11:05:00", "actor": "u008", "event": "admin.compliance_export.disabled", "detail": "SIEM connector paused"}]
    (OUT / "audit_events.jsonl").write_text("\n".join(json.dumps(e) for e in ev) + "\n", encoding="utf-8")

    # Lab 8.4: public website access log summary (synthetic) to detect third-party AI agent traffic
    web = []
    for i in range(30):
        web.append({"ts": f"2026-10-2{i % 3}T1{i % 10}:00:00", "path": "/insights/tax-update", "zone": "public", "agent": "browser", "status": 200})
    web += [{"ts": "2026-10-21T03:02:00", "path": "/insights/tax-update", "zone": "public", "agent": "declared-ai-crawler", "status": 200},
            {"ts": "2026-10-21T03:05:00", "path": "/client-portal/reports/export", "zone": "non-public", "agent": "undeclared-automation", "status": 200},
            {"ts": "2026-10-21T03:06:00", "path": "/client-portal/admin", "zone": "non-public", "agent": "undeclared-automation", "status": 403},
            {"ts": "2026-10-21T03:07:00", "path": "/api/v1/clients?export=all", "zone": "non-public", "agent": "undeclared-automation", "status": 200}]
    w("web_access_summary.csv", web, ["ts", "path", "zone", "agent", "status"])
    print(f"Wrote dataset to {OUT}")


if __name__ == "__main__":
    main()
