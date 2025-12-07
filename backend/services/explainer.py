"""
Personalized Explainer Service - Generates AI explanations
"""

import anthropic
import json
import re
from models import ExplainRequest
from config import settings, SYSTEM_PROMPT


client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


class PersonalizedExplainer:
    """Generates personalized explanations using the system prompt"""
    
    def explain(self, request: ExplainRequest) -> dict:
        """Generate explanation in specified mode"""
        
        # Format the system prompt with user data
        formatted_prompt = SYSTEM_PROMPT
        
        # Replace all placeholders
        replacements = {
            "{{user_name}}": request.user_name,
            "{{user_age}}": str(request.user_age),
            "{{user_interests_list}}": ", ".join(request.user_interests),
            "{{book_name}}": request.book_name,
            "{{book_type}}": request.book_type.value,
            "{{chapter_number}}": str(request.chapter_number),
            "{{chapter_title}}": request.chapter_title,
            "{{content_block_type}}": request.content_block_type.value,
            "{{original_content}}": request.original_content,
            "{{diagram_description}}": request.diagram_description or "None",
            "{{current_mode}}": request.mode.value.upper(),
        }
        
        for placeholder, value in replacements.items():
            formatted_prompt = formatted_prompt.replace(placeholder, value)
        
        # Add conversation history
        conv_history = ""
        if request.conversation_history:
            conv_history = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in request.conversation_history[-5:]
            ])
        formatted_prompt = formatted_prompt.replace("{{conversation_history}}", conv_history)
        
        # Add recently learned concepts
        recently_learned = ", ".join(request.recently_learned) if request.recently_learned else "None yet"
        formatted_prompt = formatted_prompt.replace("{{recently_learned_concepts}}", recently_learned)
        
        # Call Claude
        message = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
            system=formatted_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a {request.mode.value} explanation for this content."
                }
            ]
        )
        
        response_text = message.content[0].text.strip()
        
        # Parse JSON response
        try:
            response_text = re.sub(r'```json\n?|\n?```', '', response_text)
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            # If not valid JSON, return as plain text
            return {
                "mode": request.mode.value,
                "explanation": {
                    "summary": "",
                    "personalized": response_text,
                },
                "metadata": {
                    "difficulty_level": "medium",
                    "estimated_time": "3 minutes"
                }
            }