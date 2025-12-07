"""
Book Processing API Router
"""

from fastapi import APIRouter, HTTPException
from models import ParseBookRequest, ParseBookResponse
from services.book_parser import BookParser

router = APIRouter()
book_parser = BookParser()


@router.post("/parse", response_model=ParseBookResponse)
async def parse_book(request: ParseBookRequest):
    """
    Parse uploaded PDF and extract chapters + content blocks
    
    This endpoint is typically called by N8N after PDF upload
    """
    try:
        # In production, download PDF from Supabase Storage
        # For now, this is a placeholder
        pdf_text = "Sample PDF content..."  # Replace with actual download
        
        # 1. Detect book category
        category = book_parser.detect_book_category(pdf_text, request.book_name)
        
        # 2. Extract chapters
        chapters = book_parser.extract_chapters(pdf_text, category)
        
        # 3. Extract content blocks for each chapter
        result = {
            "book_id": request.book_id,
            "category": category.value,
            "chapters": []
        }
        
        for chapter in chapters:
            content_blocks = book_parser.extract_content_blocks(
                chapter.content, 
                category
            )
            
            result["chapters"].append({
                "chapter_number": chapter.chapter_number,
                "title": chapter.title,
                "content": chapter.content,
                "order_index": chapter.order_index,
                "content_blocks": [
                    {
                        "type": block.type.value,
                        "order_index": block.order_index,
                        "original_content": block.original_content,
                        "diagram_url": block.diagram_url,
                        "diagram_description": block.diagram_description
                    }
                    for block in content_blocks
                ]
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))