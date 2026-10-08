import os
os.environ["AGENTSHIELD_ADMIN_KEY"]="test-only-secret"
os.environ["AGENTSHIELD_DB_PATH"]=":memory:"
from fastapi.testclient import TestClient
from app.main import app
import tempfile
def test_gateway_default_deny_and_review():
    with tempfile.TemporaryDirectory() as d:
        os.environ["AGENTSHIELD_DB_PATH"]=d+"/test.db"
        c=TestClient(app); h={"X-Admin-Key":"test-only-secret"}
        assert c.get("/api/agents").status_code==401
        a=c.post("/api/agents",headers=h,json={"name":"Quote Agent"}).json()["id"]
        r=c.post("/api/gateway/check",headers=h,json={"agent_id":a,"action":"contract.send"}).json()
        assert r["decision"]=="block"
        assert c.put("/api/policies",headers=h,json={"agent_id":a,"action":"contract.send","decision":"review"}).status_code==200
        r=c.post("/api/gateway/check",headers=h,json={"agent_id":a,"action":"contract.send"}).json()
        assert r["decision"]=="review" and r["approval_id"]
        assert c.post("/api/approvals/"+r["approval_id"]+"/approved",headers=h).status_code==200
        assert c.put("/api/agents/"+a+"/enabled?enabled=false",headers=h).status_code==200
        assert c.post("/api/gateway/check",headers=h,json={"agent_id":a,"action":"contract.send"}).json()["decision"]=="block"
