from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai.models import AIChatRequest, ApprovalRequest, DocumentDraftRequest, VentureCreateRequest
from ai.service import ai_service

app = FastAPI(title="Apex Executive OS", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health() -> Dict[str, str]:
    return {"status": "ok", "service": "apex-executive", "version": "0.1.0"}


@app.get("/api/overview")
async def overview() -> Dict[str, Any]:
    return {
        "company": "Apex Executive OS",
        "status": "ready",
        "revenue_mtd": 214850,
        "approvals_pending": 3,
        "threats_blocked": 1842,
        "active_ventures": [
            {"id": "V-101", "sector": "Trade", "title": "Titanium Arbitrage", "projected_profit": 54200, "status": "Pipeline"},
            {"id": "V-102", "sector": "Biotech", "title": "Oncology Program", "projected_profit": 120000, "status": "In review"},
            {"id": "V-103", "sector": "Real Estate", "title": "Austin Logistics Park", "projected_profit": 84000, "status": "Approved"},
        ],
        "pending_approvals": [
            {"id": "APR-104", "title": "Release Letter of Credit", "division": "Trade", "amount": 126000, "status": "Pending"},
            {"id": "APR-221", "title": "Board Memo Draft Approval", "division": "Legal", "amount": 0, "status": "Pending"},
            {"id": "APR-309", "title": "Austin Closing SOW", "division": "Real Estate", "amount": 84000, "status": "Pending"},
        ],
    }


@app.post("/api/ai/briefing")
async def briefing(req: AIChatRequest) -> Dict[str, Any]:
    return await ai_service.briefing(req.message, req.context or "")


@app.post("/api/ai/draft")
async def draft_document(req: DocumentDraftRequest) -> Dict[str, Any]:
    return await ai_service.draft_document(req.title, req.body)


@app.post("/api/approvals")
async def create_approval(req: ApprovalRequest) -> Dict[str, Any]:
    if not req.action or not req.reason:
        raise HTTPException(status_code=400, detail="Action and reason are required.")

    return {
        "status": "pending",
        "approval_id": f"apr_{req.entity_id or 'new'}",
        "action": req.action,
        "requested_by": req.requested_by,
        "requires_human_approval": True,
    }


@app.post("/api/ventures")
async def create_venture(req: VentureCreateRequest) -> Dict[str, Any]:
    return {
        "status": "created",
        "venture": {
            "id": f"V-{len(req.title) % 1000:03d}",
            "sector": req.sector,
            "title": req.title,
            "projected_profit": req.projected_profit,
            "status": req.status,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
