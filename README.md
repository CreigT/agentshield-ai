# 🛡️ AgentShield AI — V1
**Sponsored by CREIGNIFICENT LLC**

An executable, single-administrator **AI agent security policy gateway** and mobile-responsive operations dashboard.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AGENTSHIELD_ADMIN_KEY="replace-with-long-random-secret"
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and enter your admin key.

## V1 features
- Register agents and enable/disable them
- Per-agent action policies: allow / review / block
- Default-deny gateway checks
- Pending human approval records with owner approve/reject
- Persistent SQLite audit trail and security dashboard
- Automated policy workflow test

## Important security limitations
**Development release, not production-ready.** Gateway checks return decisions; they do not intercept or execute external agent tools. Agents must be explicitly integrated, and a protected executor must enforce each decision. Approving a review record does **not** authorize a later tool execution automatically. Emergency stop blocks checks at this gateway only. Admin access uses a shared key; no user accounts, RBAC, tenant isolation, rate limiting, tamper-evident logs, or production database. SQLite requires persistent storage and is unsuitable for ephemeral serverless deployment.

Do not expose this instance publicly or connect real customer data until authentication, persistent storage, security controls, and execution enforcement are implemented.

## Tests
```bash
pip install -r requirements.txt
pytest -q
```

## Next
Add secure per-agent credentials, tool execution proxy with server-side enforcement, scoped one-time approval tokens, tenant-isolated PostgreSQL, and audited deployment.
