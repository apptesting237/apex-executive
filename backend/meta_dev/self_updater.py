import os
from typing import Any, Dict, List, Optional

try:
    from supabase import create_client, Client
except Exception:  # pragma: no cover
    Client = Any  # type: ignore
    create_client = None


class EnterpriseBrainDB:
    """Supabase-backed enterprise memory with a local in-memory fallback."""

    def __init__(self) -> None:
        self.memory_store: List[Dict[str, Any]] = []
        self.ventures_table: List[Dict[str, Any]] = [
            {
                "id": "v_trade_01",
                "sector": "Global Import / Export",
                "title": "Grade-5 Titanium Billet Cross-Border Arbitrage",
                "projected_profit": 54200.0,
                "status": "Customs Transit",
                "doc_ref": "trade_bol",
            },
            {
                "id": "v_med_01",
                "sector": "Biotech & Medical Advisory",
                "title": "Targeted Oncology Biomarker Synthesis",
                "projected_profit": 120000.0,
                "status": "Term Sheet Executed",
                "doc_ref": "medical_protocol",
            },
            {
                "id": "v_re_01",
                "sector": "Commercial Real Estate",
                "title": "Austin Industrial Logistics Park (42k sq ft)",
                "projected_profit": 84000.0,
                "status": "Closing Ready",
                "doc_ref": "realestate_dcf",
            },
        ]
        self.approvals_table: List[Dict[str, Any]] = [
            {
                "id": "appr_trade_01",
                "title": "Release $126,000 Letter of Credit for Grade-5 Titanium",
                "division": "Import & Export Trade Floor",
                "amount": 54200.0,
                "status": "Pending",
                "details": "Contract pre-sold to German aerospace buyer. Net profit: +$54,200.",
            },
            {
                "id": "appr_code_01",
                "title": "Self-Evolution: Hot-Deploy Speculative Router v5.0.0",
                "division": "Autonomous Meta-Dev",
                "amount": 0.0,
                "status": "Pending",
                "details": "Reduces multi-agent latency by 42%. 184/184 tests passed.",
            },
            {
                "id": "appr_re_01",
                "title": "Execute Austin Logistics Park Closing Memorandum",
                "division": "Commercial Real Estate",
                "amount": 84000.0,
                "status": "Pending",
                "details": "Underwritten at 21.4% 5-Yr IRR. $84,000 Sponsor fee due.",
            },
        ]

        self.supabase_url = os.getenv("SUPABASE_URL", "")
        self.supabase_key = os.getenv("SUPABASE_KEY", "")
        self.client: Optional[Client] = None
        if self.supabase_url and self.supabase_key and create_client is not None:
            self.client = create_client(self.supabase_url, self.supabase_key)
            self.ensure_schema()

    def ensure_schema(self) -> None:
        if not self.client:
            return
        schema_sql = [
            """
            create table if not exists agents (
                id uuid primary key default gen_random_uuid(),
                name text not null,
                division text not null,
                role text not null,
                status text default 'active',
                metadata jsonb default '{}'::jsonb,
                created_at timestamptz default now()
            );
            """,
            """
            create table if not exists tasks (
                id uuid primary key default gen_random_uuid(),
                title text not null,
                division text not null,
                status text default 'queued',
                owner text,
                payload jsonb default '{}'::jsonb,
                created_at timestamptz default now()
            );
            """,
            """
            create table if not exists approvals (
                id uuid primary key default gen_random_uuid(),
                approval_id text not null unique,
                title text not null,
                division text not null,
                amount numeric default 0,
                status text default 'pending',
                details text,
                created_at timestamptz default now()
            );
            """,
            """
            create table if not exists conversations (
                id uuid primary key default gen_random_uuid(),
                party text not null,
                channel text not null,
                transcript text not null,
                metadata jsonb default '{}'::jsonb,
                created_at timestamptz default now()
            );
            """,
            """
            create table if not exists artifacts (
                id uuid primary key default gen_random_uuid(),
                artifact_type text not null,
                title text not null,
                content jsonb default '{}'::jsonb,
                owner text,
                created_at timestamptz default now()
            );
            """,
            """
            create extension if not exists vector;
            create table if not exists agent_memories (
                id uuid primary key default gen_random_uuid(),
                agent_name text not null,
                department text not null,
                project text default 'enterprise',
                security_tier text default 'internal',
                embedding vector(1536),
                metadata jsonb default '{}'::jsonb,
                created_at timestamptz default now()
            );
            """,
            """
            create index if not exists idx_agent_memories_department on agent_memories (department);
            create index if not exists idx_agent_memories_project on agent_memories (project);
            """,
        ]
        for statement in schema_sql:
            try:
                self.client.rpc("exec_sql", {"query": statement}).execute()  # type: ignore[attr-defined]
            except Exception:
                pass

    async def get_all_ventures(self) -> List[Dict[str, Any]]:
        return self.ventures_table

    async def add_venture(self, venture: Dict[str, Any]) -> Dict[str, Any]:
        self.ventures_table.insert(0, venture)
        return venture

    async def get_pending_approvals(self) -> List[Dict[str, Any]]:
        return [item for item in self.approvals_table if item["status"] == "Pending"]

    async def resolve_approval(self, approval_id: str, approved: bool, feedback: Optional[str] = None) -> Dict[str, Any]:
        for item in self.approvals_table:
            if item["id"] == approval_id:
                item["status"] = "Approved" if approved else "Rejected"
                item["ceo_feedback"] = feedback
                return item
        return {"error": "approval_not_found"}

    async def query_vector_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if self.client:
            try:
                result = self.client.table("agent_memories").select("*").limit(limit).execute()
                rows = getattr(result, "data", []) or []
                if rows:
                    return rows
            except Exception:
                pass
        return [
            {"title": "EVFTA Customs Form EUR.1 Guidelines", "similarity": 0.94},
            {"title": "KRAS-G12D Computational Binding Model", "similarity": 0.89},
            {"title": "Austin Industrial Zone Feasibility", "similarity": 0.87},
            {"title": "Executive Brain Memory Search", "similarity": 0.82},
        ][:limit]

    async def record_agent_memory(self, agent_name: str, department: str, project: str, metadata: Dict[str, Any], embedding: Optional[List[float]] = None) -> Dict[str, Any]:
        item = {
            "agent_name": agent_name,
            "department": department,
            "project": project,
            "metadata": metadata,
        }
        if embedding:
            item["embedding"] = embedding
        self.memory_store.append(item)
        return item

    async def get_agents(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Dr. Evelyn Vance", "division": "Chief of Staff", "role": "Executive Assistant", "status": "active"},
            {"name": "Apex Research Lab", "division": "Scientific Research", "role": "Deep Tech", "status": "active"},
            {"name": "Medical Board", "division": "Medical Advisory", "role": "Clinical Review", "status": "active"},
        ]

    async def add_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        self.memory_store.append({"type": "task", **task})
        return task


brain_db = EnterpriseBrainDB()
