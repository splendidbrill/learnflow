# PROJECT CONTEXT: LearnFlow (MVP)

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
- `user_progress`: user_id, block_id, is_completed