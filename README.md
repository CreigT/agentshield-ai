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

## SECURE

- Gateway returns decisions only. It does not execute external tools or intercept agents automatically.
- Default-deny is applied to checks.
- Human approval is required for review actions. Approval does not auto-authorize subsequent execution.
- Admin endpoints require the shared AGENTSHIELD_ADMIN_KEY.
- Audit trail is written to SQLite. V1 has no RBAC, tenant isolation, or tamper-evident logging.
- Development release. Not production-ready.

## VERIFY

Verification is evidence of decision recording and the non-execution boundary.

- Blocked actions are recorded and rejected.
- Review actions stay pending until explicit admin action.
- Approving a review does not trigger automatic tool execution.
- Emergency stop affects only this gateway.
- Admin key is required for management.

See `docs/VERIFY_WALKTHROUGH.md` for the concrete steps. Full operational card: `docs/OPERATIONAL_CARD.md`.

## DOCUMENT

- Operational card: `docs/OPERATIONAL_CARD.md`
- Verification walkthrough: `docs/VERIFY_WALKTHROUGH.md`
- Documentation defines the V1 decision-only boundary; production enforcement requires the protected executor described in the operational card.
