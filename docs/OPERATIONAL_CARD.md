# AgentShield AI Operational Card
**Single-administrator AI agent security policy gateway and operations dashboard**  
Sponsored by CREIGNIFICENT LLC · Status: Development release; gateway returns decisions only

## Purpose
Register agents, apply per-agent allow/review/block policies, enforce default-deny checks, queue human approvals, and maintain a persistent SQLite audit trail. Decisions are returned to the caller; the gateway does not itself execute external tools.

## Trust Boundaries
- Gateway checks return decisions (allow/review/block). They do not intercept or execute external agent tools.
- Agents must be explicitly integrated; a protected executor must enforce each decision.
- Approving a review record does not automatically authorize a later tool execution.
- Emergency stop blocks checks at this gateway only.
- Admin access uses a shared key. No user accounts, RBAC, tenant isolation, rate limiting, or tamper-evident logs in V1.
- SQLite requires persistent storage; unsuitable for ephemeral serverless without volume.
- Development release, not production-ready.

## Current Enforcement (V1)
- Agent registration and enable/disable.
- Per-agent action policies: allow / review / block.
- Default-deny gateway checks.
- Pending human approval records with owner approve/reject.
- Persistent SQLite audit trail and dashboard.
- Automated policy workflow test.

## Explicit Non-Goals
- Does not execute tools or intercept external agents automatically.
- Does not provide multi-user RBAC or tenant isolation.
- Does not use a production-grade database or tamper-evident logging.
- Approval of a review does not equal authorization of subsequent execution.

## Verification Points
1. A blocked action returns block and is recorded in the audit trail.
2. A review action remains pending until an admin approves or rejects it.
3. Approving a review does not cause automatic tool execution.
4. Emergency stop prevents further checks at this gateway.
5. Admin key is required for management endpoints.

## Next Secure Step
Add a protected executor that enforces decisions server-side, introduce scoped one-time approval tokens, move to tenant-isolated PostgreSQL, and implement proper authentication before any public or customer exposure.
