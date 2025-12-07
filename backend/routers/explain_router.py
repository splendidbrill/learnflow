"""
Explanation Generation API Router
"""

from fastapi import APIRouter, HTTPException
from models import ExplainRequest, ExplanationResponse
from services.explainer import PersonalizedExplainer

router = APIRouter()
explainer = PersonalizedExplainer()


@router.post("/", response_model=ExplanationResponse)
async def generate_explanation(request: ExplainRequest):
    """
    Generate personalized explanation for a content block
    
    Supports multiple modes: explain, verify, connect, story, adaptive
    """
    try:
        result = explainer.explain(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))