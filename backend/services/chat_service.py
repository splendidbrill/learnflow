"""
Conversational Q&A Service - Handles student questions
"""

import anthropic
from models import ChatRequest
from config import settings


client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


class ConversationalQA:
    """Handles student questions about specific content blocks"""
    
    def answer_question(self, request: ChatRequest) -> str:
        """Answer student's question with context"""
        
        # Build conversation context
        system_context = f"""You are an expert tutor helping a student understand this content:

{request.original_content}

Student's interests: {", ".join(request.user_interests)}
Student's name: {request.user_name}

Guidelines:
- Answer their question clearly and concisely
- Use analogies based on their interests when helpful
- Be encouraging and supportive
- If they're confused, try a different explanation approach
- Keep responses conversational and friendly
- Don't exceed 3-4 paragraphs unless absolutely necessary"""
        
        # Format conversation history
        messages = []
        for msg in request.conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current question
        messages.append({
            "role": "user",
            "content": request.question
        })
        
        # Call Claude
        message = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=1500,
            temperature=0.7,
            system=system_context,
            messages=messages
        )
        
        return message.content[0].text