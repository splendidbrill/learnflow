"""
Pattern Detector Service - Detects solving patterns in math problems
"""

import anthropic
import json
import re
from models import PatternDetectionRequest
from config import settings


client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


class PatternDetector:
    """Detects solving patterns in math problems"""
    
    def detect_pattern(self, request: PatternDetectionRequest) -> dict:
        """Analyze example problems and create pattern card"""
        
        # Format problems
        problems_text = "\n\n".join([
            f"Problem {idx+1}:\n{prob['problem']}\n\nSolution:\n{prob['solution']}"
            for idx, prob in enumerate(request.example_problems)
        ])
        
        prompt = f"""Analyze these solved math problems and identify the common pattern/approach.

Problems:
{problems_text}

Student's interest: {request.user_interest}

Create a Pattern Card with:
1. Pattern Name (short, memorable)
2. Recognition Cues (when to use this approach)
3. Step-by-step approach (general algorithm with reasoning for each step)
4. Analogy using {request.user_interest}
5. Common mistakes students make

Return as JSON:
{{
  "pattern_name": "...",
  "recognition_cues": "...",
  "steps": [
    {{"step": 1, "action": "...", "reasoning": "..."}}
  ],
  "analogy": "...",
  "common_mistakes": ["...", "..."]
}}"""

        message = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=2000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        response_text = re.sub(r'```json\n?|\n?```', '', response_text)
        
        return json.loads(response_text)