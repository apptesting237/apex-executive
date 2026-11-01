import asyncio
import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = str(BASE_DIR / "apex_memory.db")


class EnterpriseBrainDB:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("DATABASE_PATH", DEFAULT_DB_PATH)
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ventures (
                    id TEXT PRIMARY KEY,
                    sector TEXT,
                    title TEXT,
                    projected_profit REAL,
                    status TEXT,
                    doc_ref TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS approvals (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    division TEXT,
                    amount REAL,
                    status TEXT,
                    details TEXT,
                    ceo_feedback TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    owner TEXT,
                    department TEXT,
                    priority TEXT,
                    payload TEXT,
                    status TEXT DEFAULT 'queued',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    department TEXT,
                    description TEXT,
                    similarity REAL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

            if conn.execute("SELECT COUNT(*) FROM ventures").fetchone()[0] == 0:
                conn.executemany(
                    "INSERT INTO ventures (id, sector, title, projected_profit, status, doc_ref) VALUES (?, ?, ?, ?, ?, ?)",
                    [
                        (
                            "v_trade_01",
                            "Global Import / Export",
                            "Grade-5 Titanium Billet Cross-Border Arbitrage",
                            54200.0,
                            "Customs Transit",
                            "trade_bol",
                        ),
                        (
                            "v_med_01",
                            "Biotech & Medical Advisory",
                            "Targeted Oncology Biomarker Synthesis",
                            120000.0,
                            "Term Sheet Executed",
                            "medical_protocol",
                        ),
                        (
                            "v_re_01",
                            "Commercial Real Estate",
                            "Austin Industrial Logistics Park (42k sq ft)",
                            84000.0,
                            "Closing Ready",
                            "realestate_dcf",
                        ),
                    ],
                )

            if conn.execute("SELECT COUNT(*) FROM approvals").fetchone()[0] == 0:
                conn.executemany(
                    "INSERT INTO approvals (id, title, division, amount, status, details) VALUES (?, ?, ?, ?, ?, ?)",
                    [
                        (
                            "appr_trade_01",
                            "Release $126,000 Letter of Credit for Grade-5 Titanium",
                            "Import & Export Trade Floor",
                            54200.0,
                            "Pending",
                            "Contract pre-sold to German aerospace buyer. Net profit: +$54,200.",
                        ),
                        (
                            "appr_code_01",
                            "Self-Evolution: Hot-Deploy Speculative Router v5.0.0",
                            "Autonomous Meta-Dev",
                            0.0,
                            "Pending",
                            "Reduces multi-agent latency by 42%. 184/184 tests passed.",
                        ),
                        (
                            "appr_re_01",
                            "Execute Austin Logistics Park Closing Memorandum",
                            "Commercial Real Estate",
                            84000.0,
                            "Pending",
                            "Underwritten at 21.4% 5-Yr IRR. $84,000 Sponsor fee due.",
                        ),
                    ],
                )

            if conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0] == 0:
                conn.executemany(
                    "INSERT INTO memories (title, department, description, similarity, metadata) VALUES (?, ?, ?, ?, ?)",
                    [
                        (
                            "EVFTA Customs Form EUR.1 Guidelines",
                            "trade",
                            "Cross-border customs and import-export optimization guidance.",
                            0.94,
                            json.dumps({"source": "internal"}),
                        ),
                        (
                            "KRAS-G12D Computational Binding Model",
                            "research",
                            "Biomedical modeling and therapeutic protocol validation data.",
                            0.89,
                            json.dumps({"source": "internal"}),
                        ),
                        (
                            "Austin Industrial Zone Feasibility",
                            "real_estate",
                            "Industrial logistics site underwriting and cap-rate analysis.",
                            0.87,
                            json.dumps({"source": "internal"}),
                        ),
                    ],
                )

            conn.commit()

    async def get_all_ventures(self) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._get_all_ventures)

    def _get_all_ventures(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM ventures ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in rows]

    async def add_venture(self, venture: Dict[str, Any]) -> Dict[str, Any]:
        return await asyncio.to_thread(self._add_venture, venture)

    def _add_venture(self, venture: Dict[str, Any]) -> Dict[str, Any]:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO ventures (id, sector, title, projected_profit, status, doc_ref) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    venture.get("id"),
                    venture.get("sector"),
                    venture.get("title"),
                    venture.get("projected_profit", 0.0),
                    venture.get("status", "Queued"),
                    venture.get("doc_ref", "enterprise_memorandum"),
                ),
            )
            conn.commit()
        return venture

    async def get_pending_approvals(self) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._get_pending_approvals)

    def _get_pending_approvals(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM approvals WHERE status = 'Pending' ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]

    async def resolve_approval(self, approval_id: str, approved: bool, feedback: Optional[str] = None) -> Dict[str, Any]:
        return await asyncio.to_thread(self._resolve_approval, approval_id, approved, feedback)

    def _resolve_approval(self, approval_id: str, approved: bool, feedback: Optional[str] = None) -> Dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM approvals WHERE id = ?", (approval_id,)).fetchone()
            if not row:
                return {"error": "approval_not_found"}

            status = "Approved" if approved else "Rejected"
            conn.execute(
                "UPDATE approvals SET status = ?, ceo_feedback = ? WHERE id = ?",
                (status, feedback, approval_id),
            )
            conn.commit()
            updated = dict(row)
            updated["status"] = status
            updated["ceo_feedback"] = feedback
            return updated

    async def query_vector_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._query_vector_memory, query, limit)

    def _query_vector_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT title, department, description, similarity FROM memories ORDER BY similarity DESC LIMIT ?",
                (max(1, min(limit, 10)),),
            ).fetchall()
            if rows:
                return [dict(row) for row in rows]

        return [
            {
                "title": "EVFTA Customs Form EUR.1 Guidelines",
                "department": "trade",
                "description": "Cross-border customs and import-export optimization guidance.",
                "similarity": 0.94,
            },
            {
                "title": "KRAS-G12D Computational Binding Model",
                "department": "research",
                "description": "Biomedical modeling and therapeutic protocol validation data.",
                "similarity": 0.89,
            },
            {
                "title": "Austin Industrial Zone Feasibility",
                "department": "real_estate",
                "description": "Industrial logistics site underwriting and cap-rate analysis.",
                "similarity": 0.87,
            },
        ][: max(1, min(limit, 5))]

    async def add_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return await asyncio.to_thread(self._add_task, task)

    def _add_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, owner, department, priority, payload, status) VALUES (?, ?, ?, ?, ?, 'queued')",
                (
                    task.get("title"),
                    task.get("owner"),
                    task.get("department"),
                    task.get("priority", "medium"),
                    json.dumps(task.get("payload", {})),
                ),
            )
            conn.commit()
            task["id"] = cur.lastrowid
            task["status"] = "queued"
            return task

    async def get_dashboard_summary(self) -> Dict[str, Any]:
        ventures = await self.get_all_ventures()
        approvals = await self.get_pending_approvals()
        tasks = await self.get_tasks()
        memory = await self.query_vector_memory("executive knowledge", limit=4)
        return {
            "revenue_mtd": sum(float(v.get("projected_profit", 0)) for v in ventures[:3]),
            "treasury": 1420000.0,
            "active_agents": 64,
            "pending_approvals_count": len(approvals),
            "threats_blocked": 1842,
            "active_ventures": ventures,
            "pending_approvals": approvals,
            "memory_hits": len(memory),
            "task_count": len(tasks),
        }

    async def get_tasks(self) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._get_tasks)

    def _get_tasks(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, title, owner, department, priority, payload, status FROM tasks ORDER BY id DESC LIMIT 20"
            ).fetchall()
            result = []
            for row in rows:
                item = dict(row)
                item["payload"] = json.loads(item["payload"] or "{}")
                result.append(item)
            return result

    async def record_agent_memory(
        self,
        title: str,
        department: str,
        description: str,
        similarity: float = 0.88,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = metadata or {}
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO memories (title, department, description, similarity, metadata) VALUES (?, ?, ?, ?, ?)",
                (title, department, description, similarity, json.dumps(payload)),
            )
            conn.commit()
        return {"id": cur.lastrowid, "title": title, "department": department, "similarity": similarity}


brain_db = EnterpriseBrainDB()
