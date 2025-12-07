"""
Pattern Detection API Router
"""

from fastapi import APIRouter, HTTPException
from models import PatternDetectionRequest, PatternCardResponse
from services.pattern_detector import PatternDetector

router = APIRouter()
pattern_detector = PatternDetector()


@router.post("/detect", response_model=PatternCardResponse)
async def detect_pattern(request: PatternDetectionRequest):
    """
    Detect solving patterns in math problems
    
    Analyzes 3+ example problems and creates a reusable pattern card
    """
    try:
        pattern_card = pattern_detector.detect_pattern(request)
        return pattern_card
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))