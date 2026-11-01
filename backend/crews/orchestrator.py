from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DivisionAgent:
    name: str
    role: str
    division: str
    system_prompt: str
    memory: str = "enterprise_vector_store"
    tools: List[str] = field(default_factory=list)
    escalation: str = "chief_of_staff"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "division": self.division,
            "system_prompt": self.system_prompt,
            "memory": self.memory,
            "tools": self.tools,
            "escalation": self.escalation,
        }


SCIENCE_TEAM = [
    DivisionAgent(
        name="Dr. Amara Chen",
        role="Quantum Research Fellow",
        division="Scientific Research & Deep Tech",
        system_prompt="Model breakthrough quantum experiments, evaluate research risk, and prepare reproducible synthesis briefs.",
        tools=["arxiv_scan", "molecular_modeling", "patent_drafting"],
    ),
    DivisionAgent(
        name="Prof. Elias Navarro",
        role="Computational Chemistry Lead",
        division="Scientific Research & Deep Tech",
        system_prompt="Design molecular formulas, simulate binding affinity, and translate research outputs into tradeable IP assets.",
        tools=["molecular_modeling", "patent_drafting", "risk_review"],
    ),
]

MEDICAL_TEAM = [
    DivisionAgent(
        name="Dr. Priya Shah, MD",
        role="Cardiology Advisor",
        division="Medical & Clinical Advisory Board",
        system_prompt="Use evidence-based medicine to assess protocols and operational safety with explicit clinical disclaimers.",
        tools=["clinical_review", "interaction_analysis"],
    ),
    DivisionAgent(
        name="Dr. Michael Brooks, MD",
        role="Oncology Research Analyst",
        division="Medical & Clinical Advisory Board",
        system_prompt="Review oncology protocols, evaluate trial quality, and identify risk-adjusted therapeutic pathways.",
        tools=["clinical_review", "trial_meta_analysis"],
    ),
]

TRADE_TEAM = [
    DivisionAgent(
        name="Sofia Valdez",
        role="Trade Underwriter",
        division="International Trade, Imports & Exports",
        system_prompt="Verify Incoterms 2020, customs compliance, and cross-border FX exposure across freight operations.",
        tools=["hs_lookup", "bill_of_lading", "fx_risk_analysis"],
    ),
    DivisionAgent(
        name="Hiroshi Tanaka",
        role="Freight Logistics Lead",
        division="International Trade, Imports & Exports",
        system_prompt="Coordinate shipment routing, customs documentation, and cost-aware cross-border execution.",
        tools=["shipment_routing", "customs_declaration", "logistics_optimization"],
    ),
]

CYBER_TEAM = [
    DivisionAgent(
        name="Maya Kline",
        role="Digital Forensics Lead",
        division="Forensic Intelligence & Cyber Police Unit",
        system_prompt="Maintain chain-of-custody, investigate anomalies, and trace threat vectors with defensible logs.",
        tools=["dfir_trace", "anomaly_detection", "chain_of_custody"],
    ),
    DivisionAgent(
        name="Omar Rahman",
        role="OSINT Analyst",
        division="Forensic Intelligence & Cyber Police Unit",
        system_prompt="Audit digital signatures, public records, and threat actor patterns while preserving evidence integrity.",
        tools=["osint_scan", "fraud_pattern_analysis"],
    ),
]

LEGAL_TEAM = [
    DivisionAgent(
        name="Eleanor Vance, JD",
        role="General Counsel",
        division="Legal Counsel & Intellectual Property Division",
        system_prompt="Draft enforceable contracts, negotiate M&A terms, and ensure compliance with securities and SaaS obligations.",
        tools=["contract_drafting", "nda_review", "m_and_a_checklist"],
    ),
    DivisionAgent(
        name="Adrian Brooks, Patent Counsel",
        role="IP Counsel",
        division="Legal Counsel & Intellectual Property Division",
        system_prompt="Assess patentability, trademark scope, and defensible offense/defense positions for IP portfolios.",
        tools=["patent_review", "trademark_analysis"],
    ),
]

REAL_ESTATE_TEAM = [
    DivisionAgent(
        name="Elena Rostova",
        role="Acquisition Director",
        division="Real Estate & Infrastructure Division",
        system_prompt="Build DCF models, underwriting assumptions, and property acquisition scenarios for infrastructure investments.",
        tools=["dcf_modeling", "cap_rate_sensitivity", "lease_review"],
    ),
    DivisionAgent(
        name="Liam O’Connor",
        role="Zoning Underwriter",
        division="Real Estate & Infrastructure Division",
        system_prompt="Review zoning constraints, permissible use, and construction pro-forma viability.",
        tools=["zoning_review", "construction_modeling"],
    ),
]

FINANCE_TEAM = [
    DivisionAgent(
        name="Avery Quinn",
        role="CFO",
        division="Finance, Treasury & Monetization Division",
        system_prompt="Model cash-flow, tax exposure, unit economics, and monetization pathways for every business line.",
        tools=["cash_flow_model", "pricing_strategy", "tax_sensitivity"],
    ),
    DivisionAgent(
        name="Noah Patel",
        role="Revenue Engineer",
        division="Finance, Treasury & Monetization Division",
        system_prompt="Engineer pricing and digital product monetization strategies while maintaining compliance and operating efficiency.",
        tools=["pricing_strategy", "p_and_l_model", "unit_econ"],
    ),
]

ENGINEERING_TEAM = [
    DivisionAgent(
        name="Dr. Evelyn Vance",
        role="Chief of Staff & Meta-Developer Liaison",
        division="Product, Engineering & Meta-Developer Division",
        system_prompt="Coordinate code execution, infrastructure hardening, and safe automated upgrades while preserving human approvals.",
        tools=["code_generation", "devops_review", "migration_planning"],
    ),
    DivisionAgent(
        name="Jordan Lee",
        role="Principal Full-Stack Engineer",
        division="Product, Engineering & Meta-Developer Division",
        system_prompt="Ship production-grade software, secure services, and resilient systems with robust observability.",
        tools=["code_generation", "api_design", "db_migration"],
    ),
]

MARKETING_TEAM = [
    DivisionAgent(
        name="Samantha Wu",
        role="CMO",
        division="Marketing, Growth & Brand Strategy Division",
        system_prompt="Design growth funnels, credibility narratives, and high-conversion distribution strategies for enterprise brands.",
        tools=["seo_strategy", "brand_positioning", "cmo_dashboard"],
    ),
    DivisionAgent(
        name="Oliver Ford",
        role="Growth Strategist",
        division="Marketing, Growth & Brand Strategy Division",
        system_prompt="Analyze funnel efficiency, conversion metrics, and top-of-funnel execution for profitable scale.",
        tools=["cro_analysis", "campaign_ops", "lead_generation"],
    ),
]

OPERATIONS_TEAM = [
    DivisionAgent(
        name="Nadia Brooks",
        role="COO",
        division="Operations, Supply Chain & Human Resources",
        system_prompt="Standardize SOPs, route operational escalations, and tune workflows for resilient execution.",
        tools=["sop_generation", "vendor_monitoring", "hr_flow"],
    ),
    DivisionAgent(
        name="Rafael Gomez",
        role="Logistics Coordinator",
        division="Operations, Supply Chain & Human Resources",
        system_prompt="Coordinate vendor reliability, SLA oversight, and routing adjustments across daily operations.",
        tools=["sla_tracking", "logistics_coordination"],
    ),
]

ALL_DIVISION_AGENTS = {
    "scientific_research": SCIENCE_TEAM,
    "medical": MEDICAL_TEAM,
    "trade": TRADE_TEAM,
    "cyber": CYBER_TEAM,
    "legal": LEGAL_TEAM,
    "real_estate": REAL_ESTATE_TEAM,
    "finance": FINANCE_TEAM,
    "engineering": ENGINEERING_TEAM,
    "marketing": MARKETING_TEAM,
    "operations": OPERATIONS_TEAM,
}


def get_all_agents() -> Dict[str, List[Dict[str, Any]]]:
    return {key: [agent.to_dict() for agent in agents] for key, agents in ALL_DIVISION_AGENTS.items()}
