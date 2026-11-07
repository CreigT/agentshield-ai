# VERIFY Walkthrough — Decision Does Not Equal Execution

**Goal:** Confirm the gateway returns a decision and records it, but does not execute an external tool, and that approving a review does not auto-authorize execution.

## Steps
1. Start the service with a strong AGENTSHIELD_ADMIN_KEY.
2. Register an agent and set a policy that forces review on a sample action.
3. Submit a check for that action. Confirm the response is review and a pending record is created.
4. As admin, approve the review record.
5. Confirm no external tool was invoked and no automatic execution occurred solely because of the approval.
6. Check the SQLite audit trail for the decision and approval events.

## Pass Criteria
- Decision is returned and recorded.
- No automatic tool execution follows approval.
- Audit trail contains the check and the approval.

## Fail Criteria
- Approval triggers external execution without a separate protected executor step.
- Decision is not recorded.
- Admin endpoints are accessible without the key.

This verifies the stated V1 boundary. Production enforcement requires the protected executor described in the operational card.
