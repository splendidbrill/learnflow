"""
Chat/Q&A API Router
"""

from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse
from services.chat_service import ConversationalQA

router = APIRouter()
qa_handler = ConversationalQA()


@router.post("/", response_model=ChatResponse)
async def chat_with_tutor(request: ChatRequest):
    """
    Answer student's question about a specific content block
    
    Maintains conversation context and uses student's interests
    """
    try:
        answer = qa_handler.answer_question(request)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))