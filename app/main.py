import hmac, os, sqlite3, uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app=FastAPI(title="AgentShield AI",version="1.0.0")
def auth(x_admin_key: str|None=Header(None)):
    key=os.getenv("AGENTSHIELD_ADMIN_KEY")
    if not key or not x_admin_key or not hmac.compare_digest(key,x_admin_key):
        raise HTTPException(401,"Unauthorized")
@contextmanager
def db():
    path=os.getenv("AGENTSHIELD_DB_PATH","agentshield.db")
    con=sqlite3.connect(path,timeout=15)
    con.row_factory=sqlite3.Row
    con.execute("PRAGMA busy_timeout=15000")
    con.executescript("""CREATE TABLE IF NOT EXISTS agents(id TEXT PRIMARY KEY,name TEXT NOT NULL,enabled INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS policies(agent_id TEXT NOT NULL,action TEXT NOT NULL,decision TEXT NOT NULL CHECK(decision IN ('allow','review','block')),PRIMARY KEY(agent_id,action));
CREATE TABLE IF NOT EXISTS audit(id TEXT PRIMARY KEY,at TEXT NOT NULL,agent_id TEXT NOT NULL,action TEXT NOT NULL,decision TEXT NOT NULL,reason TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS approvals(id TEXT PRIMARY KEY,agent_id TEXT NOT NULL,action TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'pending',created_at TEXT NOT NULL,reviewed_at TEXT);""")
    try:
        yield con
        con.commit()
    finally: con.close()
class Agent(BaseModel):
    name:str=Field(min_length=1,max_length=100)
class Policy(BaseModel):
    agent_id:str
    action:str=Field(min_length=1,max_length=100,pattern=r"^[a-zA-Z0-9_.:-]+$")
    decision:Literal["allow","review","block"]
class Check(BaseModel):
    agent_id:str
    action:str=Field(min_length=1,max_length=100,pattern=r"^[a-zA-Z0-9_.:-]+$")
@app.get("/",response_class=HTMLResponse)
def dashboard():
    return Path(__file__).with_name("dashboard.html").read_text(encoding="utf-8")
@app.get("/health")
def health(): return {"status":"ok","version":"1.0.0"}
@app.get("/api/agents",dependencies=[Depends(auth)])
def agents():
    with db() as c: return [dict(r) for r in c.execute("SELECT * FROM agents ORDER BY name")]
@app.post("/api/agents",dependencies=[Depends(auth)])
def add_agent(p:Agent):
    uid=str(uuid.uuid4())
    with db() as c: c.execute("INSERT INTO agents(id,name) VALUES(?,?)",(uid,p.name))
    return {"id":uid,"name":p.name,"enabled":1}
@app.put("/api/agents/{uid}/enabled",dependencies=[Depends(auth)])
def enable(uid:str,enabled:bool):
    with db() as c:
        if not c.execute("UPDATE agents SET enabled=? WHERE id=?",(int(enabled),uid)).rowcount: raise HTTPException(404,"Agent not found")
    return {"id":uid,"enabled":enabled}
@app.get("/api/policies",dependencies=[Depends(auth)])
def policies():
    with db() as c: return [dict(r) for r in c.execute("SELECT * FROM policies ORDER BY action")]
@app.put("/api/policies",dependencies=[Depends(auth)])
def policy(p:Policy):
    with db() as c:
        if not c.execute("SELECT 1 FROM agents WHERE id=?",(p.agent_id,)).fetchone(): raise HTTPException(404,"Agent not found")
        c.execute("INSERT INTO policies VALUES(?,?,?) ON CONFLICT(agent_id,action) DO UPDATE SET decision=excluded.decision",(p.agent_id,p.action,p.decision))
    return p.model_dump()
@app.post("/api/gateway/check",dependencies=[Depends(auth)])
def check(p:Check):
    with db() as c:
        agent=c.execute("SELECT enabled FROM agents WHERE id=?",(p.agent_id,)).fetchone()
        pol=c.execute("SELECT decision FROM policies WHERE agent_id=? AND action=?",(p.agent_id,p.action)).fetchone()
        if not agent: decision,reason="block","Unknown agent"
        elif not agent["enabled"]: decision,reason="block","Agent disabled"
        elif not pol: decision,reason="block","Default deny: no matching policy"
        else: decision,reason=pol["decision"],"Explicit policy"
        aid=str(uuid.uuid4()); now=datetime.now(timezone.utc).isoformat()
        c.execute("INSERT INTO audit VALUES(?,?,?,?,?,?)",(aid,now,p.agent_id,p.action,decision,reason))
        approval_id=None
        if decision=="review":
            approval_id=str(uuid.uuid4())
            c.execute("INSERT INTO approvals(id,agent_id,action,created_at) VALUES(?,?,?,?)",(approval_id,p.agent_id,p.action,now))
    return {"decision":decision,"reason":reason,"audit_id":aid,"approval_id":approval_id}
@app.get("/api/audit",dependencies=[Depends(auth)])
def audit():
    with db() as c: return [dict(r) for r in c.execute("SELECT * FROM audit ORDER BY at DESC LIMIT 100")]
@app.get("/api/approvals",dependencies=[Depends(auth)])
def approvals():
    with db() as c: return [dict(r) for r in c.execute("SELECT * FROM approvals ORDER BY created_at DESC LIMIT 100")]
@app.post("/api/approvals/{uid}/{decision}",dependencies=[Depends(auth)])
def decide(uid:str,decision:Literal["approved","rejected"]):
    with db() as c:
        if not c.execute("UPDATE approvals SET status=?,reviewed_at=? WHERE id=? AND status='pending'",(decision,datetime.now(timezone.utc).isoformat(),uid)).rowcount: raise HTTPException(404,"Pending approval not found")
    return {"id":uid,"status":decision}
