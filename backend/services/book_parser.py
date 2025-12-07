"""
Book Parser Service - Extracts structured content from PDFs
"""

import anthropic
import PyPDF2
import io
import json
import re
from typing import List
from models import BookType, Chapter, ContentBlock, ContentBlockType
from config import settings


client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


class BookParser:
    """Parses uploaded PDFs and extracts structured content"""
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract raw text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
            return text
        except Exception as e:
            raise Exception(f"PDF parsing error: {str(e)}")
    
    def detect_book_category(self, text_sample: str, book_name: str) -> BookType:
        """Use Claude to detect book category"""
        
        prompt = f"""Analyze this book and classify it into ONE category:

Categories:
- physics
- chemistry
- biology
- math
- english
- literature
- history
- geography
- civics
- self_improvement

Book Name: {book_name}
Content Sample: {text_sample[:3000]}

Respond with ONLY the category name, nothing else."""

        message = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )
        
        category = message.content[0].text.strip().lower().replace(" ", "_")
        return BookType(category)
    
    def extract_chapters(self, text: str, book_type: BookType) -> List[Chapter]:
        """Extract chapters using AI"""
        
        prompt = f"""Extract all chapters from this {book_type.value} textbook.

Text:
{text[:15000]}

Return JSON array:
[
  {{
    "chapter_number": 1,
    "title": "Introduction to Motion",
    "start_marker": "Chapter 1",
    "end_marker": "Chapter 2"
  }}
]

Only return valid JSON, no other text."""

        message = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        response_text = re.sub(r'```json\n?|\n?```', '', response_text)
        
        chapters_data = json.loads(response_text)
        
        # Extract actual content for each chapter
        chapters = []
        for idx, ch_data in enumerate(chapters_data):
            start = text.find(ch_data["start_marker"])
            end = text.find(ch_data["end_marker"]) if idx < len(chapters_data) - 1 else len(text)
            
            chapter_content = text[start:end].strip()
            
            chapters.append(Chapter(
                chapter_number=ch_data["chapter_number"],
                title=ch_data["title"],
                content=chapter_content,
                order_index=idx
            ))
        
        return chapters
    
    def extract_content_blocks(
        self, 
        chapter_content: str, 
        book_type: BookType
    ) -> List[ContentBlock]:
        """Extract paragraphs, diagrams, examples, questions"""
        
        if book_type == BookType.MATH:
            return self._extract_math_blocks(chapter_content)
        elif book_type in [BookType.PHYSICS, BookType.CHEMISTRY, BookType.BIOLOGY]:
            return self._extract_science_blocks(chapter_content)
        else:
            return self._extract_text_blocks(chapter_content)
    
    def _extract_math_blocks(self, content: str) -> List[ContentBlock]:
        """Extract math-specific content"""
        
        prompt = f"""Extract content blocks from this math chapter.

Identify:
1. Concept paragraphs (explanatory text)
2. Example problems (with "Example" or "Solved Problem")
3. Solutions (step-by-step)
4. Practice questions (problems without solutions)

Content:
{content[:10000]}

Return JSON:
[
  {{
    "type": "paragraph|example_question|solution|practice_question",
    "content": "...",
    "order_index": 0
  }}
]"""

        message = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        response_text = re.sub(r'```json\n?|\n?```', '', response_text)
        blocks_data = json.loads(response_text)
        
        blocks = []
        for block in blocks_data:
            blocks.append(ContentBlock(
                type=ContentBlockType(block["type"]),
                order_index=block["order_index"],
                original_content=block["content"]
            ))
        
        return blocks
    
    def _extract_science_blocks(self, content: str) -> List[ContentBlock]:
        """Extract science blocks with diagram detection"""
        
        prompt = f"""Extract content blocks from this science chapter.

Identify:
1. Paragraphs (text explanations)
2. Diagrams (look for "Figure X", "Diagram", or visual descriptions)
3. Example problems
4. Practice questions

Content:
{content[:10000]}

For diagrams, provide detailed descriptions.

Return JSON:
[
  {{
    "type": "paragraph|diagram|example_question|practice_question",
    "content": "...",
    "diagram_description": "..." (only for diagrams),
    "order_index": 0
  }}
]"""

        message = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        response_text = re.sub(r'```json\n?|\n?```', '', response_text)
        blocks_data = json.loads(response_text)
        
        blocks = []
        for block in blocks_data:
            blocks.append(ContentBlock(
                type=ContentBlockType(block["type"]),
                order_index=block["order_index"],
                original_content=block["content"],
                diagram_description=block.get("diagram_description")
            ))
        
        return blocks
    
    def _extract_text_blocks(self, content: str) -> List[ContentBlock]:
        """Simple paragraph extraction for humanities books"""
        
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        
        blocks = []
        for idx, para in enumerate(paragraphs):
            if len(para) > 100:  # Skip short paragraphs (likely headers)
                blocks.append(ContentBlock(
                    type=ContentBlockType.PARAGRAPH,
                    order_index=idx,
                    original_content=para
                ))
        
        return blocks