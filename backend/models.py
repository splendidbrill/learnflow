"""
Pydantic Models for Request/Response Validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


# Enums
class BookType(str, Enum):
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    MATH = "math"
    ENGLISH = "english"
    LITERATURE = "literature"
    HISTORY = "history"
    GEOGRAPHY = "geography"
    CIVICS = "civics"
    SELF_IMPROVEMENT = "self_improvement"


class ContentBlockType(str, Enum):
    PARAGRAPH = "paragraph"
    DIAGRAM = "diagram"
    EXAMPLE_QUESTION = "example_question"
    PRACTICE_QUESTION = "practice_question"
    SOLUTION = "solution"


class Mode(str, Enum):
    EXPLAIN = "explain"
    VERIFY = "verify"
    CONNECT = "connect"
    STORY = "story"
    ADAPTIVE = "adaptive"


# Request Models
class ParseBookRequest(BaseModel):
    pdf_url: str
    book_id: str
    book_name: str
    user_id: str


class ExplainRequest(BaseModel):
    content_block_id: str
    user_id: str
    user_name: str
    user_age: int
    user_interests: List[str]
    book_name: str
    book_type: BookType
    chapter_number: int
    chapter_title: str
    content_block_type: ContentBlockType
    original_content: str
    diagram_description: Optional[str] = None
    mode: Mode = Mode.EXPLAIN
    conversation_history: Optional[List[Dict[str, str]]] = None
    recently_learned: Optional[List[str]] = None


class ChatRequest(BaseModel):
    content_block_id: str
    user_id: str
    user_name: str
    user_interests: List[str]
    original_content: str
    question: str
    conversation_history: List[Dict[str, str]]


class PatternDetectionRequest(BaseModel):
    book_id: str
    chapter_id: str
    example_problems: List[Dict[str, Any]]
    user_interest: str


# Response Models
class Chapter(BaseModel):
    chapter_number: int
    title: str
    content: str
    order_index: int


class ContentBlock(BaseModel):
    type: ContentBlockType
    order_index: int
    original_content: str
    diagram_url: Optional[str] = None
    diagram_description: Optional[str] = None


class ParseBookResponse(BaseModel):
    book_id: str
    category: BookType
    chapters: List[Dict[str, Any]]


class ExplanationResponse(BaseModel):
    mode: str
    explanation: Dict[str, Any]
    verify_question: Optional[Dict[str, Any]] = None
    connections: Optional[List[Dict[str, Any]]] = None
    metadata: Dict[str, Any]


class ChatResponse(BaseModel):
    answer: str


class PatternCardResponse(BaseModel):
    pattern_name: str
    recognition_cues: str
    steps: List[Dict[str, Any]]
    analogy: str
    common_mistakes: List[str]