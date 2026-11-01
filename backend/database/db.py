from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import settings
from database.db import brain_db
from crews.orchestrator import orchestrator
from meta_dev.self_updater import meta_dev
from security.firewall import firewall


class MandateRequest(BaseModel):
    directive: str = Field(..., min_length=3, max_length=4000)
    target_division: Optional[str] = "all"


class ApprovalRequest(BaseModel):
    approval_id: str = Field(..., min_length=3)
    approved: bool
    feedback: Optional[str] = None


class VentureCreateRequest(BaseModel):
    sector: str = Field(..., min_length=2, max_length=200)
    title: str = Field(..., min_length=2, max_length=255)
    projected_profit: float = Field(..., ge=0)


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    owner: str = Field(..., min_length=2, max_length=120)
    department: str = Field(..., min_length=2, max_length=120)
    priority: str = Field(default="medium")
    payload: Dict[str, Any] = Field(default_factory=dict)


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "status": "online",
        "company": "Apex Executive",
        "ceo": "Founder",
        "version": settings.VERSION,
        "firewall": "Fortress Level 1 Active",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "uptime": "online",
    }


@app.get("/api/dashboard/summary")
async def get_dashboard_summary() -> Dict[str, Any]:
    ventures = await brain_db.get_all_ventures()
    approvals = await brain_db.get_pending_approvals()
    telemetry = firewall.get_telemetry()
    return {
        "revenue_mtd": 214850.0,
        "treasury": 1420000.0,
        "active_agents": 64,
        "pending_approvals_count": len(approvals),
        "threats_blocked": telemetry["threats_blocked"],
        "active_ventures": ventures,
        "pending_approvals": approvals,
        "memory_hits": 13,
    }


@app.get("/api/agents")
async def get_agents() -> Dict[str, Any]:
    roster = await orchestrator.get_roster()
    return {"divisions": roster, "count": sum(len(v) for v in roster.values())}


@app.get("/api/approvals")
async def get_approvals() -> Dict[str, Any]:
    items = await brain_db.get_pending_approvals()
    return {"items": items, "count": len(items)}


@app.get("/api/department-status")
async def department_status() -> Dict[str, Any]:
    return {
        "departments": [
            {"name": "Research", "status": "active", "signal": "green"},
            {"name": "Medical", "status": "review", "signal": "amber"},
            {"name": "Trade", "status": "active", "signal": "blue"},
            {"name": "Cyber", "status": "monitoring", "signal": "red"},
            {"name": "Legal", "status": "active", "signal": "green"},
            {"name": "Finance", "status": "active", "signal": "green"},
        ]
    }


@app.post("/api/ceo/mandate")
async def issue_ceo_mandate(
    req: MandateRequest,
    request: Request,
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> Dict[str, Any]:
    if not firewall.validate_bearer_token(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized: valid CEO bearer token required.")

    inspection = firewall.inspect_inbound_prompt(req.directive, ip_address=request.client.host if request.client else "unknown")
    if not inspection["safe"]:
        raise HTTPException(status_code=400, detail=inspection["reason"])

    execution = await orchestrator.execute_ceo_directive(inspection["clean_text"], req.target_division or "all")
    return {"status": "dispatched", "execution": execution}


@app.post("/api/ceo/approve")
async def process_ceo_approval(
    req: ApprovalRequest,
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> Dict[str, Any]:
    if not firewall.validate_bearer_token(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized: valid CEO bearer token required.")

    resolved = await brain_db.resolve_approval(req.approval_id, req.approved, req.feedback)
    return {"status": "resolved", "result": resolved}


@app.post("/api/ventures/create")
async def create_venture(req: VentureCreateRequest) -> Dict[str, Any]:
    venture = {
        "id": f"v_custom_{len(await brain_db.get_all_ventures()) + 1}",
        "sector": req.sector,
        "title": req.title,
        "projected_profit": req.projected_profit,
        "status": "Crew Assembled",
        "doc_ref": "enterprise_memorandum",
    }
    saved = await brain_db.add_venture(venture)
    return {"status": "created", "venture": saved}


@app.post("/api/tasks/create")
async def create_task(req: TaskCreateRequest) -> Dict[str, Any]:
    payload = {
        "title": req.title,
        "owner": req.owner,
        "department": req.department,
        "priority": req.priority,
        "payload": req.payload,
    }
    task = await brain_db.add_task(payload)
    return {"status": "queued", "task": task}


@app.get("/api/meta-dev/check-upgrade")
async def check_self_upgrade() -> Dict[str, Any]:
    return await meta_dev.scan_and_stage_upgrade()


@app.get("/api/brain/search")
async def brain_search(query: str, limit: int = 5) -> Dict[str, Any]:
    results = await brain_db.query_vector_memory(query, limit=max(1, min(10, limit)))
    return {"query": query, "results": results}


@app.post("/api/security/red-team")
async def trigger_red_team() -> Dict[str, Any]:
    return firewall.simulate_red_team_probe(25)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
