from __future__ import annotations

from typing import Any, Dict


class SafeActionRouter:
    def __init__(self):
        self.allowed_actions = {
            "briefing": "read_only",
            "risk_summary": "read_only",
            "draft_memo": "write_document",
            "approve_action": "requires_human_approval",
            "send_email": "requires_human_approval",
            "execute_budget": "requires_human_approval",
        }

    def check(self, action: str) -> Dict[str, Any]:
        policy = self.allowed_actions.get(action, "blocked")
        if policy == "blocked":
            return {"allowed": False, "reason": "Action is not in the allowlist."}
        if policy == "requires_human_approval":
            return {"allowed": False, "reason": "This action requires explicit human approval before execution."}
        return {"allowed": True, "policy": policy}


safe_action_router = SafeActionRouter()
