from __future__ import annotations

from typing import Any, Dict, List

try:
    from langchain_core.documents import Document
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import FakeEmbeddings
    LANGCHAIN_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    Document = None
    FAISS = None
    FakeEmbeddings = None
    LANGCHAIN_AVAILABLE = False

try:
    from langgraph.graph import END, START, StateGraph
    LANGGRAPH_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    StateGraph = None
    START = "__start__"
    END = "__end__"
    LANGGRAPH_AVAILABLE = False

COMPANY_KNOWLEDGE = [
    {
        "title": "Apex Executive Mission",
        "content": "Apex Executive OS helps leaders track revenue, risks, approvals, ventures, and strategic priorities. AI is advisory and every material action requires human approval.",
    },
    {
        "title": "Security policy",
        "content": "All AI access is role-scoped. Sensitive actions such as treasury, legal, or security execution require explicit human approval and audit logging.",
    },
    {
        "title": "Operating model",
        "content": "The company uses an approval queue, document drafting workflow, and executive briefing flow. AI summarizes and recommends while leadership approves actions.",
    },
    {
        "title": "Risk posture",
        "content": "Free-tier LLMs are useful for experimentation but vary in reliability and quota. The app must track confidence, fallback providers, and human review requirements.",
    },
]


class RAGService:
    def __init__(self, knowledge: List[Dict[str, str]] | None = None):
        self.documents = knowledge or COMPANY_KNOWLEDGE
        self.vector_store = None

        if LANGCHAIN_AVAILABLE and Document is not None and FAISS is not None and FakeEmbeddings is not None:
            docs = [
                Document(page_content=item["content"], metadata={"title": item["title"]})
                for item in self.documents
            ]
            self.vector_store = FAISS.from_documents(docs, FakeEmbeddings(size=256))

    def retrieve(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        if self.vector_store is not None:
            matches = self.vector_store.similarity_search(query, k=limit)
            return [
                {"title": item.metadata.get("title", "Knowledge"), "content": item.page_content}
                for item in matches
            ]

        lowered_query = query.lower()
        scores: List[tuple[int, Dict[str, str]]] = []
        for item in self.documents:
            score = 0
            text = f"{item['title']} {item['content']}".lower()
            for token in lowered_query.split():
                if token in text:
                    score += 2
            if score > 0:
                scores.append((score, item))

        scores.sort(key=lambda pair: pair[0], reverse=True)
        ranked = [item for _, item in scores[:limit]]
        if not ranked:
            ranked = [self.documents[0]]
        return [{"title": item["title"], "content": item["content"]} for item in ranked]

    def build_answer(self, question: str, context: str = "") -> Dict[str, Any]:
        results = self.retrieve(question)
        evidence = "\n\n".join(f"- {item['title']}: {item['content']}" for item in results)
        answer = (
            f"Based on the company knowledge base, here is a safe response to: '{question}'\n\n"
            f"{evidence}\n\n"
            "Recommended action: keep this as an advisory recommendation and require explicit human approval before any material action."
        )
        if context.strip():
            answer += f"\n\nAdditional context: {context.strip()}"
        return {"answer": answer, "sources": results, "model": "rag-safe-briefing"}


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
            return {"answer": result.get("answer", ""), "sources": result.get("retrieved", self.rag.retrieve(question)), "model": "langgraph-advisor"}
        return self.rag.build_answer(question, context)


rag_service = RAGService()
langgraph_advisor = LangGraphAdvisor()
