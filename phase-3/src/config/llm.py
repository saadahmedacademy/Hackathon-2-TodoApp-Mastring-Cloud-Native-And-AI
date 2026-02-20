# phase-3/src/config/llm.py
from openai import OpenAI
from . import settings

def get_gemini_openai_client():
    """
    Initializes and returns an OpenAI client configured to use
    the Gemini (via OpenAI-compatible endpoint) model.
    """
    client = OpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url=settings.GEMINI_BASE_URL,
    )
    return client
