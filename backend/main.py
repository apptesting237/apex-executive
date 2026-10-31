"""
Apex Executive AI Enterprise Backend
FastAPI server connecting the mobile cockpit to CrewAI multi-agent crews,
the AI Application Firewall, and the Enterprise Brain database.
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio

from config import settings
from database.db import brain_db
from security.firewall import firewall
from meta_dev.self_updater import meta_dev
from crews.orchestrator import orchestrator

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MandateRequest(BaseModel):
    directive: str
    target_division: Optional[str] = "all"

class ApprovalRequest(BaseModel):
    approval_id: str
    approved: bool
    feedback: Optional[str] = None

class VentureCreateRequest(BaseModel):
    sector: str
    title: str
    profit: float

@app.get("/")
def root():
    return {
        "status": "online",
        "company": "Apex Global Holdings",
        "ceo": "Founder",
        "version": settings.VERSION,
        "firewall": "Fortress Level 1 Active"
    }

@app.get("/api/dashboard/summary")
async def get_dashboard_summary():
    ventures = await brain_db.get_all_ventures()
    approvals = await brain_db.get_pending_approvals()
    telemetry = firewall.get_telemetry()
    return {
        "revenue_mtd": 214850.00,
        "treasury": 1420000.00,
        "active_agents": 64,
        "pending_approvals_count": len(approvals),
        "threats_blocked": telemetry["threats_blocked"],
        "active_ventures": ventures,
        "pending_approvals": approvals
    }

@app.post("/api/ceo/mandate")
async def issue_ceo_mandate(req: MandateRequest):
    # 1. Inspect prompt through AI Application Firewall
    inspection = firewall.inspect_inbound_prompt(req.directive)
    if not inspection["safe"]:
        raise HTTPException(status_code=400, detail=inspection["reason"])
    
    # 2. Dispatch to Chief of Staff & Crew Orchestrator
    result = await orchestrator.execute_ceo_directive(inspection["clean_text"], req.target_division)
    return {"status": "dispatched", "execution": result}

@app.post("/api/ceo/approve")
async def process_ceo_approval(req: ApprovalRequest):
    result = await brain_db.resolve_approval(req.approval_id, req.approved, req.feedback)
    return {"status": "resolved", "result": result}

@app.post("/api/ventures/create")
async def create_venture(req: VentureCreateRequest):
    new_v = {
        "id": f"v_custom_{len(await brain_db.get_all_ventures()) + 1}",
        "sector": req.sector,
        "title": req.title,
        "projected_profit": req.profit,
        "status": "Crew Assembled",
        "doc_ref": "trade_bol"
    }
    saved = await brain_db.add_venture(new_v)
    return {"status": "created", "venture": saved}

@app.post("/api/security/red-team")
def trigger_red_team():
    return firewall.simulate_red_team_probe(25)

@app.get("/api/meta-dev/check-upgrade")
async def check_self_upgrade():
    return await meta_dev.scan_and_stage_upgrade()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
