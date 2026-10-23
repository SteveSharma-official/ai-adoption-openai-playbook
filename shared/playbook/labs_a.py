"""Lab engines for Parts I and II (Chapters 0 to 8).

Every function takes the merged lab config and the lab folder, and returns
(Result, title, report sections, extra evidence files or None).
The checks model the decisions the book teaches. They do not call OpenAI; optional API and workspace steps are documented in each README.
"""
from __future__ import annotations
import re, statistics, datetime as dt
from .core import new, ds, users, groups, md_table, dump
from .common import parse_ts, parse_date

SECRET = re.compile(r"(sk-(proj-|svcacct-|admin-)?[A-Za-z0-9_\-]{20,}|-----BEGIN (RSA )?PRIVATE KEY-----)")
TODAY = dt.date(2026, 10, 23)


# ---------- Chapter 0 ----------
def quick_start(cfg, lab):
    r = new("0.1", "Quick Start and Lab Safety Check")
    env = cfg.get("environment", {})
    for p in [p for p in lab.rglob("*") if p.is_file() and "evidence" not in p.parts]:
        if SECRET.search(p.read_text(encoding="utf-8", errors="ignore")):
            r.find("secret-in-config", f"{p.name} contains something that looks like an API key. Keys live in an environment variable or a secrets manager, never in a file.")
    if env.get("target") not in ("local", "sandbox"):
        r.find("non-sandbox-target", f"target is '{env.get('target')}'. Labs run locally or in a dedicated sandbox project only.")
    if not ds("users.csv"):
        r.find("dataset-missing", "Run python shared/scripts/generate_datasets.py")
    r.data["environment"] = env
    return r, "Quick Start and Lab Safety Check", [("Environment", dump(env))], None


LEVELS = {2: ["named_use_case", "business_owner", "risk_assessment", "data_boundary"],
          3: ["production_kpis", "identity_controls", "logging", "evaluation", "escalation_path"],
          4: ["shared_platform", "central_governance", "enterprise_observability", "reusable_agents"],
          5: ["cross_platform_orchestration", "adaptive_governance"]}


def maturity(cfg, lab):
    r = new("0.2", "AI Adoption Maturity Self-Assessment")
    have = {k for k, v in (cfg.get("evidence") or {}).items() if v}
    level, gaps = 1, []
    for lv in sorted(LEVELS):
        missing = [k for k in LEVELS[lv] if k not in have]
        if missing:
            gaps.append({"level": lv, "missing": ", ".join(missing)})
            break
        level = lv
    claimed = int(cfg.get("claimed_level", 1))
    r.data.update(claimed=claimed, evidenced=level)
    if claimed > level:
        r.find("maturity-overclaim", f"Claimed level {claimed} but evidence supports level {level}. The next question to answer is at level {level + 1}.")
    rows = [{"level": lv, "requires": ", ".join(k), "met": all(x in have for x in k)} for lv, k in LEVELS.items()]
    return r, "AI Adoption Maturity Self-Assessment", [("Scored levels", md_table(rows, ["level", "requires", "met"])),
                                                       ("First gap", md_table(gaps, ["level", "missing"]))], None


# ---------- Chapter 1 ----------
def seat_value(cfg, lab):
    """Active seats are not value. The renewal case must rest on measured workflows, not message counts."""
    r = new("1.1", "Seat Utilisation and Value Baseline")
    us = users()
    rows, by_user = ds("workspace_usage.csv"), {}
    for x in rows:
        by_user.setdefault(x["user_id"], []).append(x)
    seats = int(cfg["seats"])
    active = sum(1 for u, xs in by_user.items() if statistics.mean(int(x["active_days"]) for x in xs) >= cfg.get("active_days_threshold", 4))
    measured = sum(1 for u, xs in by_user.items() if any(x["in_measured_workflow"] == "yes" for x in xs))
    leavers = [s for s in cfg.get("assigned_seats", []) if us.get(s, {}).get("status") == "leaver"]
    r.data.update(seats=seats, active=active, in_measured_workflow=measured)
    case = cfg["renewal_case"]
    if case.get("evidence_type") in ("messages", "active_users", "logins") or not case.get("measured_workflows"):
        r.find("vanity-renewal-case", f"The renewal case rests on {case.get('evidence_type')}. {active} of {seats} seats are active, but only {measured} users work in a measured workflow. Value needs a workflow, a baseline and an owner.")
    for wf in case.get("measured_workflows") or []:
        if not wf.get("baseline") or not wf.get("owner"):
            r.find("workflow-without-baseline", f"{wf.get('name')}: a measured workflow needs a baseline and an owner.")
    if leavers:
        r.find("seats-assigned-to-leavers", f"Seats are still assigned to leavers: {', '.join(leavers)}.")
    if case.get("seats_requested", seats) > seats and active / seats < 0.6:
        r.find("expansion-without-utilisation", f"Expansion to {case['seats_requested']} seats requested while only {active} of {seats} are active.", blocking=False)
    summary = [{"seats": seats, "active (>= threshold days per month)": active, "in a measured workflow": measured}]
    return r, "Seat Utilisation and Value Baseline", [("Utilisation", md_table(summary, list(summary[0]))), ("Renewal case", dump(case))], None


def cycle_hours():
    ev = {}
    for e in ds("engagement_letter_events.csv"):
        ev.setdefault(e["case_id"], {})[e["step"]] = parse_ts(e["ts"])
    return statistics.median((v["signed"] - v["received"]).total_seconds() / 3600 for v in ev.values())


def process_baseline(cfg, lab):
    r = new("1.2", "Process Baseline and the 90-Day Plan")
    p = cfg["plan"]
    measured = round(cycle_hours(), 1)
    r.data["measured_median_hours"] = measured
    if p.get("baseline_hours") in (None, ""):
        r.find("no-baseline", f"No baseline recorded. Measured median cycle time from the event log is {measured} hours.")
    elif abs(float(p["baseline_hours"]) - measured) / measured > 0.10:
        r.find("baseline-mismatch", f"Recorded baseline {p['baseline_hours']} differs from measured {measured} by more than 10%.")
    if not p.get("business_owner"):
        r.find("no-owner", "The process has no named business owner.")
    if not p.get("day_90_gate"):
        r.find("no-day-90-gate", "There is no Day 90 Gate date. A pilot without a decision date becomes a perpetual pilot.")
    if p.get("target_hours") and p.get("baseline_hours") and float(p["target_hours"]) >= float(p["baseline_hours"]):
        r.find("target-not-improvement", "The target is not better than the baseline.")
    return r, "Process Baseline and the 90-Day Plan", [("Plan", dump(p)), ("Measured", f"Median engagement letter cycle time: **{measured} hours** (40 synthetic cases).")], None


# ---------- Chapter 2 ----------
def portfolio(cfg, lab):
    r = new("2.1", "Enterprise AI Portfolio Map")
    plats = cfg["platforms"]
    rows = []
    for w in cfg["workloads"]:
        p = plats.get(w["platform"])
        home = [n for n, x in plats.items() if w["data_location"] in x.get("home_data", [])]
        if not p:
            r.find("unknown-platform", f"{w['id']}: {w['platform']} is not on the map.")
            continue
        if not p.get("sanctioned"):
            r.find("unsanctioned-platform", f"{w['id']}: {w['platform']} is not sanctioned for enterprise data.")
        if home and w["platform"] not in home and not w.get("justification"):
            r.find("placement-unjustified", f"{w['id']}: data lives in {w['data_location']} (natural home {', '.join(home)}) but is placed on {w['platform']} with no written justification.")
        if w.get("archetype") not in cfg["archetypes"]:
            r.find("no-archetype", f"{w['id']}: workload archetype '{w.get('archetype')}' is not one of {', '.join(cfg['archetypes'])}.")
        rows.append({"workload": w["id"], "archetype": w.get("archetype", ""), "data": w["data_location"], "platform": w["platform"], "home": ", ".join(home), "justification": w.get("justification", "")})
    mmd = "flowchart LR\n" + "\n".join(f"  {x['workload'].replace('-', '_')}[{x['workload']}] --> {x['platform'].replace(' ', '_')}" for x in rows)
    return r, "Enterprise AI Portfolio Map", [("Placements", md_table(rows, ["workload", "archetype", "data", "platform", "home", "justification"]))], {"portfolio-map.mmd": mmd}


def shadow_ai(cfg, lab):
    r = new("2.2", "Shadow AI Discovery")
    dec = cfg.get("decisions") or {}
    signals = []
    for p in ds("proxy_ai_summary.csv"):
        if p["account_type"] == "personal":
            signals.append({"signal": f"{p['domain']} (personal accounts)", "source": "proxy", "users": p["users"], "key": p["domain"]})
    for g in ds("oauth_grants.csv") + (cfg.get("new_grants") or []):
        if g["sanctioned"] == "no":
            signals.append({"signal": g["app"], "source": f"app consent ({g['scopes']})", "users": g["users"], "key": g["app"]})
    for e in ds("expense_ai_lines.csv"):
        signals.append({"signal": e["vendor"], "source": f"expense {e['claim']}", "users": 1, "key": e["vendor"]})
    rows = []
    for s in signals:
        d = dec.get(s["key"], {})
        if not d.get("decision"):
            r.find("unreviewed-ai-signal", f"{s['signal']} ({s['source']}, {s['users']} users) has no decision.")
        elif d["decision"] in ("review", "migrate") and not d.get("owner"):
            r.find("no-owner", f"{s['signal']} is marked {d['decision']} with no named owner.")
        rows.append({**s, "decision": d.get("decision", ""), "owner": d.get("owner", "")})
    return r, "Shadow AI Discovery", [("Signals and decisions", md_table(rows, ["signal", "source", "users", "decision", "owner"]))], None


# ---------- Chapter 3 ----------
VANITY = re.compile(r"(prompt|message|active user|seat|licen[cs]e|usage|adoption rate|session|login)", re.I)


def value_hypothesis(cfg, lab):
    r = new("3.1", "Value Hypothesis and Baseline")
    h = cfg["hypothesis"]
    if VANITY.search(h.get("metric", "")) or h.get("metric_type") == "activity":
        r.find("vanity-metric", f"'{h.get('metric')}' measures activity, not a business number the CFO recognises.")
    if h.get("value_category") not in ("time returned", "quality improved", "capability unlocked"):
        r.find("no-value-category", "Name the value category: time returned, quality improved or capability unlocked.")
    if h.get("baseline") in (None, ""):
        r.find("no-baseline", "No measured baseline.")
    elif h.get("target") not in (None, "") and h.get("direction", "down") == "down" and float(h["target"]) >= float(h["baseline"]):
        r.find("target-not-improvement", "Target does not improve on the baseline.")
    if not h.get("measured_by"):
        r.find("no-measurement-source", "No system of record named for measurement.")
    if not h.get("owner"):
        r.find("no-owner", "No accountable business owner.")
    return r, "Value Hypothesis and Baseline", [("Hypothesis", dump(h))], None


# ---------- Chapter 4 ----------
RUNGS = ["Seats", "Workspace build", "API", "Frontier", "Host"]


def minimum_rung(w):
    if w.get("sovereign_hosting_required"):
        return "Host"
    if w.get("multi_system_autonomous_agent"):
        return "Frontier"
    if w.get("integrates_with_enterprise_systems"):
        return "API"
    if w.get("repeatable_team_workflow"):
        return "Workspace build"
    return "Seats"


def decision_ladder(cfg, lab):
    r = new("4.1", "The Decision Ladder")
    rows = []
    for w in cfg["workloads"]:
        m, c = minimum_rung(w), w["chosen_rung"]
        if RUNGS.index(c) > RUNGS.index(m) and not w.get("justification"):
            r.find("over-engineered", f"{w['id']}: chose {c}, minimum is {m}, and no justification is recorded. Every rung up adds cost, ownership and attack surface.")
        if RUNGS.index(c) < RUNGS.index(m):
            r.find("under-scoped", f"{w['id']}: chose {c} but the workload needs at least {m}.")
        if c == "Frontier" and not w.get("frontier_access_confirmed"):
            r.find("platform-availability-unconfirmed", f"{w['id']}: Frontier had limited availability at the time of writing. Confirm access before you design around it.", blocking=False)
        rows.append({"workload": w["id"], "minimum": m, "chosen": c, "justification": w.get("justification", "")})
    return r, "The Decision Ladder", [("Rungs", md_table(rows, ["workload", "minimum", "chosen", "justification"]))], None


# ---------- Chapter 5 ----------
LAYERS = ("workspace", "workspace_builds", "api_platform", "agent_platform", "governance")


def architecture(cfg, lab):
    r = new("5.1", "Reference Architecture as Code")
    a = cfg["architecture"]
    for layer in LAYERS:
        if not a["layers"].get(layer):
            r.find("missing-layer", f"Layer '{layer}' has no components. Draw it, even if it is empty or locked.")
    for c in a["components"]:
        for k, rule in (("identity", "no-identity"), ("owner", "no-owner"), ("logging", "no-logging"), ("data_boundary", "no-data-boundary")):
            if not c.get(k):
                r.find(rule, f"{c['name']} has no {k.replace('_', ' ')}.")
        if c.get("identity") == "shared-api-key":
            r.find("shared-key-identity", f"{c['name']} authenticates with a shared API key. Nobody can say which team acted.")
    lines = ["flowchart TB"]
    for layer, comps in a["layers"].items():
        lines.append(f"  subgraph {layer}")
        lines += [f"    {layer}_{i}[\"{c}\"]" for i, c in enumerate(comps)]
        lines.append("  end")
    return r, "Reference Architecture as Code", [("Components", md_table(a["components"], ["name", "layer", "identity", "owner", "logging", "data_boundary"]))], {"reference-architecture.mmd": "\n".join(lines)}


def key_audit(cfg, lab):
    r = new("5.2", "Identity Model and API Key Audit")
    keys = {k["key_id"]: dict(k) for k in ds("api_keys.json")}
    for k in cfg.get("new_keys") or []:
        keys[k["key_id"]] = dict(k)
    for kid, ch in (cfg.get("key_changes") or {}).items():
        if kid in keys:
            keys[kid].update(ch)
    for kid in cfg.get("revoked") or []:
        keys.pop(kid, None)
    us = users()
    rows = []
    for k in keys.values():
        age = (TODAY - parse_date(k["created"])).days
        if len(k["used_by"]) > 1:
            r.find("shared-key", f"{k['key_id']} is used by {', '.join(k['used_by'])}. One identity per workload, or no one can say who acted.")
        if k["permissions"] == "all" and k["type"] != "service_account":
            r.find("over-scoped-key", f"{k['key_id']} has all permissions. Use restricted, project-scoped keys.")
        if k["stored_in"] not in ("secret_manager", "env_var"):
            r.find("key-in-code", f"{k['key_id']} is stored in {k['stored_in']}.")
        if us.get(k["owner"], {}).get("status") != "active":
            r.find("leaver-owned-key", f"{k['key_id']} is owned by {k['owner']}, who is not an active employee.")
        if age > cfg.get("max_key_age_days", 180):
            r.find("stale-key", f"{k['key_id']} is {age} days old.", blocking=False)
        rows.append({"key": k["key_id"], "project": k["project"], "type": k["type"], "permissions": k["permissions"], "owner": k["owner"], "used_by": ", ".join(k["used_by"]), "stored_in": k["stored_in"]})
    return r, "Identity Model and API Key Audit", [("Key inventory", md_table(rows, ["key", "project", "type", "permissions", "owner", "used_by", "stored_in"]))], None


# ---------- Chapter 6 ----------
def _builds(cfg):
    b = {x["build_id"]: dict(x) for x in ds("workspace_builds.json")}
    for x in cfg.get("new_builds") or []:
        b[x["build_id"]] = dict(x)
    for bid, ch in (cfg.get("build_changes") or {}).items():
        if bid in b:
            b[bid].update(ch)
    return b


def build_exposure(cfg, lab):
    r = new("6.1", "Workspace Build Exposure Report")
    labels = {f["file_id"]: f for f in ds("knowledge_files.csv")}
    rows = []
    for b in _builds(cfg).values():
        broad = b["sharing"] in ("workspace", "link")
        for kf in b["knowledge"]:
            f = labels[kf]
            if f["label"] == "Restricted" and (broad or b["sharing"] not in cfg["allowed_groups_for_restricted"]):
                r.find("restricted-content-exposed", f"{b['name']} ({b['type']}) holds '{f['title']}' (Restricted) and is shared {b['sharing']}. Anyone who can use the build can ask it about the file.", build=b["build_id"])
            elif f["label"] == "Confidential" and b["sharing"] == "link":
                r.find("confidential-link-share", f"{b['name']} holds Confidential content and is shared by link.", blocking=False)
        rows.append({"build": b["build_id"], "name": b["name"], "type": b["type"], "sharing": b["sharing"], "knowledge": ", ".join(labels[k]["label"] for k in b["knowledge"])})
    return r, "Workspace Build Exposure Report", [("Builds", md_table(rows, ["build", "name", "type", "sharing", "knowledge"]))], None


def gpt_migration(cfg, lab):
    """Custom GPTs retire (dates per OpenAI notices; verify for your workspace). Every GPT needs an owner, a decision and a plan for custom actions, which do not migrate."""
    r = new("6.2", "GPT Retirement and Plugin Migration Register")
    us = users()
    reg = cfg.get("register") or {}
    deadline = parse_date(cfg["retirement_date"])
    rows = []
    for b in _builds(cfg).values():
        if b["type"] != "gpt":
            continue
        e = reg.get(b["build_id"], {})
        d = e.get("decision")
        if not d:
            r.find("no-migration-decision", f"{b['name']}: no decision (migrate to plugin, rebuild as workspace agent, or retire) before {deadline}.")
            continue
        owner = e.get("owner") or b["owner"]
        if us.get(owner, {}).get("status") != "active":
            r.find("orphaned-gpt", f"{b['name']}: owner {owner} has left. Only the creator or an admin can migrate it.")
        if d in ("plugin", "workspace_agent") and b["custom_actions"] and not e.get("actions_plan"):
            r.find("custom-actions-unplanned", f"{b['name']}: custom actions ({', '.join(b['custom_actions'])}) do not migrate to plugins. Rebuild them as an app action or MCP server, or drop them.")
        if e.get("target_date") and parse_date(e["target_date"]) > deadline:
            r.find("after-retirement", f"{b['name']}: target date {e['target_date']} is after retirement on {deadline}.")
        rows.append({"gpt": b["name"], "decision": d, "owner": owner, "custom_actions": ", ".join(b["custom_actions"]), "target": e.get("target_date", "")})
    return r, "GPT Retirement and Plugin Migration Register", [("Register", md_table(rows, ["gpt", "decision", "owner", "custom_actions", "target"]))], None


PATTERNS = {"tfn": re.compile(r"\b\d{3}\s?\d{3}\s?\d{3}\b"), "card": re.compile(r"\b(?:\d{4}[\s-]?){3}\d{4}\b"),
            "medicare": re.compile(r"\b\d{4}\s?\d{5}\s?\d\b")}


def prompt_content(cfg, lab):
    r = new("6.3", "Prompt Content Check on a Compliance Export")
    rules = {x["pattern"]: x for x in cfg.get("dlp_rules") or []}
    rows = []
    for m in ds("compliance_messages.jsonl"):
        hits = [k for k, rx in PATTERNS.items() if rx.search(m["text"])]
        for h in hits:
            ru = rules.get(h)
            if not ru or ru.get("action") not in ("block", "redact"):
                r.find("sensitive-identifier-in-prompt", f"{m['conv']}: a {h} pattern reached the model and no blocking or redacting rule covers it.")
        rows.append({"conversation": m["conv"], "user": m["user_id"], "patterns": ", ".join(hits) or "none"})
    ret = cfg.get("retention_days")
    if ret is None or ret > cfg.get("max_retention_days", 365):
        r.find("retention-unset", f"Workspace retention is {ret}. Set it to the shortest period your records policy allows.")
    if not cfg.get("export_to", None):
        r.find("no-compliance-export", "No Compliance API export to your DLP or SIEM. Detection needs the data to leave the platform.")
    return r, "Prompt Content Check on a Compliance Export", [("Messages scanned", md_table(rows, ["conversation", "user", "patterns"])),
                                                              ("Rules", md_table(list(rules.values()), ["pattern", "action", "tool"]))], None


# ---------- Chapter 7 ----------
def authority_gateway(cfg, lab):
    r = new("7.1", "Human-Agent Authority Matrix Gateway")
    m = cfg["matrix"]
    rows = []
    for q in cfg["requests"]:
        rule = m["actions"].get(q["action"])
        if q.get("channel") == "direct" and not m.get("gateway_only"):
            outcome = "executed (bypassed gateway)"
            r.find("gateway-bypass", f"{q['id']}: {q['action']} reached the system directly. The agent's identity must only reach tools through the gateway.")
        elif q.get("channel") == "direct":
            outcome = "rejected: network policy allows gateway only"
        elif not rule:
            outcome = "denied: action not in matrix"
        elif rule["agent"] == "never":
            outcome = "denied: human only"
        elif rule["agent"] == "approval" and q.get("amount", 0) > rule.get("auto_limit", 0) and not q.get("approval"):
            outcome = "held for approval"
        else:
            outcome = "executed"
            if q.get("consequential") and not q.get("approval") and q.get("amount", 0) > m.get("consequential_threshold", 0):
                r.find("unapproved-consequential-action", f"{q['id']}: {q['action']} for {q.get('amount')} executed with no human approval.")
        rows.append({"request": q["id"], "action": q["action"], "amount": q.get("amount", ""), "channel": q.get("channel", "gateway"), "outcome": outcome})
    for act in m.get("human_only", []):
        if m["actions"].get(act, {}).get("agent") != "never":
            r.find("matrix-invariant", f"{act} must be 'never' for agents.")
    return r, "Human-Agent Authority Matrix Gateway", [("Decisions", md_table(rows, ["request", "action", "amount", "channel", "outcome"]))], None


SENSITIVE_ACTIONS = ("send_email", "create_calendar_event", "edit_spreadsheet", "post_message", "create_record")


def workspace_agent_review(cfg, lab):
    r = new("7.2", "Workspace Agent Permission Review")
    policy = cfg["policy"]
    rows = []
    for b in _builds(cfg).values():
        if b["type"] != "workspace_agent":
            continue
        if b["personal_credentials"] and b["sharing"] != "private" and not policy.get("allow_shared_personal_credentials"):
            r.find("shared-agent-on-personal-credentials", f"{b['name']} is shared ({b['sharing']}) and acts with its builder's personal credentials. Everyone who runs it acts as the builder.")
        for act, on in (b.get("approvals") or {}).items():
            if act in SENSITIVE_ACTIONS and not on:
                r.find("approval-off-for-sensitive-action", f"{b['name']}: approval is off for {act}.")
        for app in b["apps"]:
            if app not in policy["allowed_apps"]:
                r.find("app-not-allowed", f"{b['name']} uses {app}, which is not on the allowed list.")
        rows.append({"agent": b["name"], "sharing": b["sharing"], "personal_credentials": b["personal_credentials"], "apps": ", ".join(b["apps"]), "approvals": dump(b.get("approvals"))[8:-4]})
    return r, "Workspace Agent Permission Review", [("Workspace agents", md_table(rows, ["agent", "sharing", "personal_credentials", "apps", "approvals"])), ("Policy", dump(policy))], None


# ---------- Chapter 8 ----------
def inventory(cfg, lab):
    r = new("8.1", "Agent Register")
    found = ds("agents.json") + (cfg.get("discovered_extra") or [])
    reg = {x["agent_id"]: x for x in cfg["register"]}
    us = users()
    rows = []
    for a in found:
        e = reg.get(a["agent_id"])
        if not e:
            r.find("unregistered-agent", f"{a['name']} ({a['surface']}) exists but is not in the Agent Register.")
            continue
        if us.get(e.get("owner"), {}).get("status") != "active":
            r.find("orphaned-agent", f"{a['name']}: owner {e.get('owner')} is not an active employee.")
        if not e.get("risk_tier"):
            r.find("no-risk-tier", f"{a['name']} has no risk tier.")
        if not e.get("identity"):
            r.find("no-identity", f"{a['name']} has no recorded identity (user, builder, key, service account or agent identity).")
        rows.append({**a, "owner": e.get("owner"), "risk_tier": e.get("risk_tier", ""), "identity": e.get("identity", "")})
    return r, "Agent Register", [("Register reconciliation", md_table(rows, ["agent_id", "name", "surface", "owner", "risk_tier", "identity"]))], None


ASI = {"ASI01": "Agent goal hijack", "ASI02": "Tool misuse and exploitation", "ASI03": "Identity and privilege abuse",
       "ASI04": "Agentic supply chain vulnerabilities", "ASI05": "Unexpected code execution", "ASI06": "Memory and context poisoning",
       "ASI07": "Insecure inter-agent communication", "ASI08": "Cascading failures", "ASI09": "Human-agent trust exploitation",
       "ASI10": "Rogue agents"}


def threat_model(cfg, lab):
    r = new("8.2", "OWASP Agentic Threat Model")
    cat = set(cfg["control_catalogue"])
    rows = []
    for k, name in ASI.items():
        t = (cfg.get("threats") or {}).get(k) or {}
        ctl = t.get("controls") or []
        if not ctl:
            r.find("unmitigated-threat", f"{k} {name} has no control.")
        for c in ctl:
            if c not in cat:
                r.find("unknown-control", f"{k} cites '{c}', which is not in the control catalogue.")
        if ctl and not t.get("owner"):
            r.find("no-owner", f"{k} has controls but no owner.")
        rows.append({"id": k, "risk": name, "controls": ", ".join(ctl), "owner": t.get("owner", "")})
    return r, "OWASP Agentic Threat Model", [("Threat to control map", md_table(rows, ["id", "risk", "controls", "owner"]))], None


def detection(cfg, lab):
    r = new("8.3", "Logging, Detection and the Kill Switch")
    logs = ds("audit_events.jsonl")
    rules = cfg["rules"]
    alerts = []
    for e in logs:
        for ru in rules:
            k = ru["type"]
            hit = ((k == "action_without_approval" and e["event"] == "app.action" and not e.get("approval")) or
                   (k == "token_spike" and e.get("tokens", 0) > ru.get("threshold", 10 ** 12)) or
                   (k == "key_created" and e["event"] == "admin.api_key.created") or
                   (k == "export_disabled" and e["event"] == "admin.compliance_export.disabled"))
            if hit:
                alerts.append({"rule": ru["id"], "ts": e["ts"], "actor": e["actor"], "event": e["event"]})
    suspicious = {e["ts"] for e in logs if e["event"] != "agent.run"}
    for ts in sorted(suspicious - {a["ts"] for a in alerts}):
        r.find("undetected-event", f"Suspicious event at {ts} raised no alert.")
    lg = cfg["logging"]
    if not lg.get("compliance_export_enabled") or lg.get("retention_days", 0) < 365:
        r.find("logging-gap", f"Compliance export enabled={lg.get('compliance_export_enabled')}, SIEM retention {lg.get('retention_days')} days. Keep agent activity for at least 365 days outside the platform.")
    ks = cfg["kill_switch"]
    if not ks.get("last_tested") or (TODAY - parse_date(ks["last_tested"])).days > 90:
        r.find("kill-switch-untested", "The kill switch has not been tested in the last 90 days.")
    return r, "Logging, Detection and the Kill Switch", [("Alerts", md_table(alerts, ["rule", "ts", "actor", "event"])), ("Kill switch", dump(ks))], None


CONTRACT = ["incident_notification_hours", "notify_affected_organisation", "agent_activity_logs_on_request", "named_security_contact", "independent_assurance_report"]


def supplier_readiness(cfg, lab):
    """The Medicare lesson: a supplier's agent can touch your systems, and you may hear about it from the news. Contract for notice; detect it yourself."""
    r = new("8.4", "AI Supplier Incident Readiness")
    c = cfg["contract"]
    for k in CONTRACT:
        if not c.get(k):
            r.find("contract-gap", f"The AI supplier agreement does not cover '{k.replace('_', ' ')}'.")
    if c.get("incident_notification_hours") and int(c["incident_notification_hours"]) > cfg["max_notification_hours"]:
        r.find("notification-too-slow", f"Notification within {c['incident_notification_hours']} hours exceeds your maximum of {cfg['max_notification_hours']}.")
    det = cfg["detection"]
    rows = []
    for e in ds("web_access_summary.csv"):
        if e["zone"] == "non-public" and e["agent"] == "undeclared-automation":
            caught = det.get("flag_undeclared_automation_on_non_public")
            if not caught:
                r.find("agent-traffic-undetected", f"{e['ts']} automated access to {e['path']} (status {e['status']}) raised no alert.")
            rows.append({"ts": e["ts"], "path": e["path"], "status": e["status"], "alerted": bool(caught)})
    if not cfg.get("inbox", {}).get("monitored_24x7"):
        r.find("unmonitored-security-inbox", "The address suppliers will notify is not monitored around the clock.")
    return r, "AI Supplier Incident Readiness", [("Contract terms", dump(c)), ("Automated access to non-public paths", md_table(rows, ["ts", "path", "status", "alerted"]))], None


REGISTRY = {"0.1": quick_start, "0.2": maturity, "1.1": seat_value, "1.2": process_baseline, "2.1": portfolio,
            "2.2": shadow_ai, "3.1": value_hypothesis, "4.1": decision_ladder, "5.1": architecture, "5.2": key_audit,
            "6.1": build_exposure, "6.2": gpt_migration, "6.3": prompt_content, "7.1": authority_gateway, "7.2": workspace_agent_review,
            "8.1": inventory, "8.2": threat_model, "8.3": detection, "8.4": supplier_readiness}
