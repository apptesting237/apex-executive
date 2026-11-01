from __future__ import annotations

from typing import Any, Dict, List

from config import settings
from database.db import brain_db
from llm import generate_llm_response


class EnterpriseCrewOrchestrator:
    def __init__(self):
        self.roster = {
            "Chief of Staff": ["Dr. Evelyn Vance", "Memo Engine", "Executive Risk Desk"],
            "Finance": ["Treasury Monitor", "Capital Allocation Crew"],
            "Research": ["Neural Discovery Lab", "Biomedical Ops"],
            "Operations": ["Trade Floor", "Supply Chain Prioritizer"],
            "Cyber": ["Zero-Trust Firewall", "Threat Hunting Cell"],
        }

    async def get_roster(self) -> Dict[str, List[str]]:
        return self.roster

    async def execute_ceo_directive(self, mandate: str, division: str = "all") -> Dict[str, Any]:
        prompt = (
            f"You are the Apex Executive orchestration layer. "
            f"Create a concise operational response for this mandate: {mandate}. "
            f"Target division: {division}. "
            "Return a JSON object with keys: division, action, summary, profit_projected, risk_level, next_steps."
        )
        raw = generate_llm_response(prompt, system="You are the CEO command intelligence layer for Apex Executive.")

        if raw.get("live"):
            text = raw["text"]
        else:
            text = (
                "{\"division\": \"Chief of Staff\", \"action\": \"Dispatch strategic briefing packet\", "
                "\"summary\": \"Your mandate has been decomposed into executive workstreams and routed to the relevant operating crews.\", "
                "\"profit_projected\": 54000, \"risk_level\": \"low\", \"next_steps\": [\"Confirm target division\", \"Queue approvals\", \"Publish brief\"]}"
            )

        try:
            import json

            payload = json.loads(text)
        except Exception:
            payload = {
                "division": division or "Chief of Staff",
                "action": "Dispatch strategic briefing packet",
                "summary": text,
                "profit_projected": 54000,
                "risk_level": "low",
                "next_steps": ["Confirm target division", "Queue approvals", "Publish brief"],
            }

        await brain_db.record_agent_memory(
            title=f"Mandate: {mandate[:60]}",
            department=payload.get("division", division or "Chief of Staff"),
            description=payload.get("summary", mandate),
            similarity=0.91,
            metadata={"mandate": mandate},
        )

        return {
            "division": payload.get("division", division or "Chief of Staff"),
            "action": payload.get("action", "Dispatch strategic briefing packet"),
            "summary": payload.get("summary", "Mandate routed to the operating crews."),
            "profit_projected": payload.get("profit_projected", 54000),
            "risk_level": payload.get("risk_level", "low"),
            "next_steps": payload.get("next_steps", ["Queue approvals", "Publish brief"]),
            "provider": raw.get("provider", "local"),
        }


orchestrator = EnterpriseCrewOrchestrator()
