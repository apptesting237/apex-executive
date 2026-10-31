# This file intentionally documents the safe first-version architecture for the Apex Executive MVP.

## Overview
Apex Executive is a company dashboard and AI advisory workspace. It is designed for executive workflows, venture tracking, approvals, and team-level operational summaries. The app is intentionally conservative: AI can analyze and draft, but approved humans must trigger material actions.

## Core principles
- AI is advisory, not autonomous.
- Approval workflow is mandatory for configuration changes, financial actions, and legal actions.
- Security and data access are role-scoped.
- Free LLMs are useful for prototyping but their reliability varies.
- Audit logs are required for every operational action.

## MVP features
- Executive dashboard with summary metrics
- Active ventures view
- Pending approvals list
- Risk and compliance panel
- Rich text board notes editor
- AI advisor panel with safe responses
- RAG and LangGraph-ready architecture for future enhancements

## Tech stack
- Frontend: React + Vite
- Backend: FastAPI
- AI layer: RAG + optional LangGraph scaffolding
- LLM gateway: FreeLLMAPI-compatible OpenAI endpoint
- Deployment target: local Docker Desktop and later cloud deployment

## Safe AI workflow
1. User sends a question or requests a recommendation.
2. Backend runs a scoped retrieval step over company knowledge.
3. AI drafts a human-readable recommendation.
4. Approval gateway checks if action is allowed.
5. For material actions, the system requires explicit sign-off.
6. Every approved action is logged with actor, time, and reason.

## Run locally
### Frontend
```
cd web
npm install
npm run dev
```
### Backend
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
### Docker Desktop
```
docker compose up --build
```

## Local URLs
- Frontend: http://localhost:5173
- Backend health: http://localhost:8000/health
