from __future__ import annotations

from typing import Any, Dict, List

try:
    from langchain_core.documents import Document
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import FakeEmbeddings
    LANGCHAIN_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency path
    Document = None  # type: ignore
    ChatPromptTemplate = None  # type: ignore
    StrOutputParser = None  # type: ignore
    FAISS = None  # type: ignore
    FakeEmbeddings = None  # type: ignore
    LANGCHAIN_AVAILABLE = False

try:
    from langgraph.graph import END, START, StateGraph
    LANGGRAPH_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency path
    StateGraph = None  # type: ignore
    START = "__start__"  # type: ignore
    END = "__end__"  # type: ignore
    LANGGRAPH_AVAILABLE = False


COMPANY_KNOWLEDGE = [
    {
        "title": "Apex Executive Mission",
        "content": "Apex Executive OS helps leaders track revenue, risks, approvals, ventures, and strategic priorities. The system uses AI for summaries and recommendations, but all material actions require human approval.",
    },
    {
        "title": "Security policy",
        "content": "AI access is scoped by role and department. No autonomous execution of treasury, legal, or security actions is allowed without explicit approval.",
    },
    {
        "title": "Operational policy",
        "content": "The company uses an approval queue, audit logging, and structured reporting. Every recommendation should be evidence based and explainable.",
    },
    {
        "title": "Risk posture",
        "content": "Free-tier LLM availability changes frequently, so the system should prefer fallback providers and maintain a clear recommendation with a confidence note.",
    },
    {
        "title": "Product scope",
        "content": "The MVP includes dashboard metrics, project tracking, document drafting, approvals, and a guided AI assistant for executive workflows.",
    },
]


class RAGService:
    def __init__(self, knowledge: List[Dict[str, str]] | None = None):
        self.documents = knowledge or COMPANY_KNOWLEDGE
        self.vector_store = None
        if LANGCHAIN_AVAILABLE and FAISS and FakeEmbeddings:
            docs = [Document(page_content=item["content"], metadata={"title": item["title"]}) for item in self.documents]
            self.vector_store = FAISS.from_documents(docs, FakeEmbeddings(size=256))

    def retrieve(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        if self.vector_store is not None:
            matches = self.vector_store.similarity_search(query, k=limit)
            return [
                {"title": item.metadata.get("title", "Knowledge"), "content": item.page_content}
                for item in matches
            ]

        query_lower = query.lower()
        scored = []
        for item in self.documents:
            score = 0
            for token in query_lower.split():
                if token in item["title"].lower():
                    score += 3
                if token in item["content"].lower():
                    score += 1
            scored.append({"score": score, "item": item})
        ranked = sorted(scored, key=lambda entry: entry["score"], reverse=True)
        return [
            {"title": entry["item"]["title"], "content": entry["item"]["content"]}
            for entry in ranked[:limit]
            if entry["score"] > 0
        ] or [{"title": self.documents[0]["title"], "content": self.documents[0]["content"]}]

    def build_answer(self, question: str, context: str = "") -> Dict[str, Any]:
        results = self.retrieve(question)
        evidence = "\n\n".join(f"- {item['title']}: {item['content']}" for item in results)
        final_answer = (
            f"Based on the current company knowledge base, here is a safe response for: '{question}'\n\n"
            f"{evidence}\n\n"
            f"Recommended action: keep this as an advisory recommendation. Only approve material actions after human review."
        )
        if context.strip():
            final_answer += f"\n\nAdditional context: {context.strip()}"

        return {
            "answer": final_answer,
            "sources": results,
            "model": "rag-safe-briefing",
        }


class LangGraphAdvisor:
    def __init__(self):
        self.rag = RAGService()

    def build_graph(self):
        if not LANGGRAPH_AVAILABLE or StateGraph is None:
            return None

        workflow = StateGraph(dict)
        workflow.add_node("retrieve", lambda state: {**state, "retrieved": self.rag.retrieve(state["question"])})
        workflow.add_node("draft", lambda state: {**state, "answer": self.rag.build_answer(state["question"], state.get("context", ""))["answer"]})
        workflow.add_edge("retrieve", "draft")
        workflow.set_entry_point("retrieve")
        workflow.add_edge("draft", END)
        return workflow.compile()

    async def answer(self, question: str, context: str = "") -> Dict[str, Any]:
        graph = self.build_graph()
        if graph is not None:
            result = graph.invoke({"question": question, "context": context})
            return {
                "answer": result.get("answer", ""),
                "sources": result.get("retrieved", self.rag.retrieve(question)),
                "model": "langgraph-advisor",
            }
        return self.rag.build_answer(question, context)


rag_service = RAGService()
langgraph_advisor = LangGraphAdvisor()
