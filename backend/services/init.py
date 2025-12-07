"""
Services package initialization
"""

from .book_parser import BookParser
from .explainer import PersonalizedExplainer
from .chat_service import ConversationalQA
from .pattern_detector import PatternDetector

__all__ = ["BookParser", "PersonalizedExplainer", "ConversationalQA", "PatternDetector"]