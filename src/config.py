from dotenv import load_dotenv
import os

class MissingAPIKeyError(Exception):
    """Raised when the FRED API key is missing."""
    pass

def get_fred_api_key() -> str:
    load_dotenv()  # loads variables from .env
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise MissingAPIKeyError("FRED API key not found in environment.")
    return api_key
