"""
Configuration and Environment Variables
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # Anthropic
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")
    
    # N8N Webhooks
    N8N_WEBHOOK_URL: str = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook")
    
    # System Prompt Path
    SYSTEM_PROMPT_PATH: str = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.md")
    
    # Upload Settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [".pdf"]
    
    # AI Settings
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7


settings = Settings()


def load_system_prompt() -> str:
    """Load the system prompt from file"""
    try:
        with open(settings.SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise Exception(f"System prompt not found at {settings.SYSTEM_PROMPT_PATH}")


# Load system prompt at startup
SYSTEM_PROMPT = load_system_prompt()