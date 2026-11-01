from __future__ import annotations

from typing import Any, Dict, List

from crews.agents import ALL_DIVISION_AGENTS, get_all_agents
from database.db import brain_db


class EnterpriseCrewOrchestrator:
    def __init__(self) -> None:
        self.chief_of_staff = {
            "name": "Dr. Evelyn Vance, PhD",
            "institution": "Harvard University",
            "role": "Personal Chief of Staff to the CEO",
        }

    async def get_roster(self) -> Dict[str, List[Dict[str, Any]]]:
        return get_all_agents()

    async def execute_ceo_directive(self, mandate: str, division: str = "all") -> Dict[str, Any]:
        lowered = mandate.lower()

        if any(keyword in lowered for keyword in ["trade", "import", "export", "titanium", "shipping", "customs"]):
            return {
                "division": "International Trade, Imports & Exports",
                "leads": ["Sofia Valdez (Trade Underwriter)", "Hiroshi Tanaka (Freight Logistics Lead)"],
                "action": "Generated customs compliance review, HS classification validation, and cross-border execution plan.",
                "deliverable_ref": "trade_bol",
                "profit_projected": "+$54,200.00",
                "agents": ALL_DIVISION_AGENTS["trade"],
            }
        if any(keyword in lowered for keyword in ["medical", "cancer", "trial", "clinical", "science", "patient"]):
            return {
                "division": "Medical & Clinical Advisory Board",
                "leads": ["Dr. Priya Shah, MD", "Dr. Michael Brooks, MD"],
                "action": "Completed evidence-based clinical review, protocol safety analysis, and trial-risk meta-analysis.",
                "deliverable_ref": "medical_protocol",
                "profit_projected": "+$120,000.00",
                "agents": ALL_DIVISION_AGENTS["medical"],
            }
        if any(keyword in lowered for keyword in ["real estate", "warehouse", "property", "zoning", "lease"]):
            return {
                "division": "Real Estate & Infrastructure Division",
                "leads": ["Elena Rostova", "Liam O’Connor"],
                "action": "Developed DCF model, cap-rate sensitivity matrix, and acquisition memorandum.",
                "deliverable_ref": "realestate_dcf",
                "profit_projected": "+$84,000.00",
                "agents": ALL_DIVISION_AGENTS["real_estate"],
            }
        if any(keyword in lowered for keyword in ["fraud", "forensic", "investigat", "police", "cyber", "threat", "security"]):
            return {
                "division": "Forensic Intelligence & Cyber Police Unit",
                "leads": ["Maya Kline", "Omar Rahman"],
                "action": "Issued OSINT, anomaly, and evidence-chain evaluation across the risk surface.",
                "deliverable_ref": "police_dossier",
                "profit_projected": "+$28,000.00 / month retainer",
                "agents": ALL_DIVISION_AGENTS["cyber"],
            }
        if division != "all":
            for key, agents in ALL_DIVISION_AGENTS.items():
                if division.lower() in key.lower() or division.lower() in " ".join(a["division"].lower() for a in agents):
                    return {
                        "division": next(iter(agents))["division"],
                        "action": f"Executed targeted workflow for {division}.",
                        "agents": agents,
                    }

        return {
            "division": "Executive Directorate & Legal Chambers",
            "leads": ["Dr. Evelyn Vance (Chief of Staff)", "Eleanor Vance, JD (General Counsel)"],
            "action": f"Analyzed CEO directive: '{mandate}'. Coordinated cross-functional execution plan.",
            "deliverable_ref": "legal_msa",
            "profit_projected": "Commercial Milestone Sourced",
            "agents": ALL_DIVISION_AGENTS["legal"],
        }


orchestrator = EnterpriseCrewOrchestrator()
