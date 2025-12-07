<!-- # PROJECT CONTEXT: LearnFlow (MVP)

## CORE OBJECTIVE
A Next.js + React Native learning app where users upload PDFs. The system parses the PDF into "Content Blocks" (paragraphs/diagrams). Users click a block to get a personalized explanation (analogy-based) using the "Sherlock Dash Alpha" LLM via OpenRouter.

## TECH STACK
- **Frontend:** Next.js 14 (App Router) + React Native (Expo)
- **Backend:** Python FastAPI (Port 8000)
- **Database:** Supabase (Postgres)
- **AI Engine:** OpenRouter (`openrouter/sherlock-dash-alpha`)
- **Orchestration:** n8n (Scheduling & Notifications only)

## CRITICAL RULES
1. **JSON Only:** All AI endpoints must return strict JSON.
2. **Stateless:** Do not rely on server memory; all state is in Supabase.
3. **Chunking:** Text must be stored in `content_blocks` table (paragraph level).
4. **No Hallucinations:** If a library (like LlamaParse) is missing, fail gracefully.

## DATABASE SCHEMA SUMMARY
- `profiles`: user_id, interests (jsonb)
- `books`: id, title, pdf_url
- `content_blocks`: id, book_id, original_text, explanation (jsonb), type (text/image)
- `user_progress`: user_id, block_id, is_completed -->

# PROJECT: LearnFlow (MVP) Context

## 1. CORE OBJECTIVE
AI Tutor app. Users upload PDFs -> parsed to blocks -> explanations via OpenRouter (Auto-Fallback).

## 2. TECH STACK
- **Frontend:** Next.js 14 (App Router), Tailwind, Framer Motion, Lucide React.
- **Backend:** Python FastAPI (Port 8000).
- **Database:** Supabase (Postgres) + Row Level Security (RLS).
- **AI Engine:** OpenRouter (Llama 3.2 -> Gemini 2.0 Flash -> Fallbacks).
- **Orchestration:** n8n (Scheduler - pending).

## 3. KEY FILES & STRUCTURE
- `backend/main.py`: Entry point.
- `backend/services/explainer.py`: AI Logic (JSON output only).
- `backend/services/book_parser.py`: PDF -> Text Blocks (`pypdf`).
- `frontend/app/dashboard/page.tsx`: User Library.
- `frontend/app/book/[id]/page.tsx`: Reading Interface.

## 4. API ENDPOINTS (Backend)
- `POST /api/upload-book` (Form Data: title, user_id, file)
- `POST /api/explain` (JSON: text, interests, book_type)

## 5. DATABASE SCHEMA
- `profiles`: id (FK auth.users), interests (jsonb).
- `books`: id, user_id, total_blocks, processed (bool).
- `content_blocks`: id, book_id, original_content, cached_explanation.

## 6. CURRENT STATUS
- Backend: ✅ Complete & Verified.
- Frontend: 🚧 In Progress (Landing Page & Dashboard).