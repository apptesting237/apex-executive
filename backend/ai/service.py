from __future__ import annotations

from typing import Any, Dict

from ai.rag_service import langgraph_advisor, rag_service
from ai.safety import safe_action_router


class ApexAIService:
    def __init__(self) -> None:
        self.rag = rag_service
        self.workflow = langgraph_advisor

    async def briefing(self, question: str, context: str = "") -> Dict[str, Any]:
        action_check = safe_action_router.check("briefing")
        if not action_check["allowed"]:
            return {"answer": action_check["reason"], "sources": [], "model": "blocked"}
        return await self.workflow.answer(question, context)

    async def draft_document(self, title: str, body: str) -> Dict[str, Any]:
        action_check = safe_action_router.check("draft_memo")
        if not action_check["allowed"]:
            return {"status": "blocked", "message": action_check["reason"]}
        return {
            "status": "draft_saved",
            "title": title,
            "snippet": body[:220],
            "requires_human_approval": True,
        }


ai_service = ApexAIService()
