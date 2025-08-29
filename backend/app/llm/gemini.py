import json
import time

from typing import Dict, Any
from google import generativeai as genai
from google.api_core import exceptions as google_exceptions

from app.config import settings

_model = None

def _get_model():
    global _model
    if _model is None:
        genai.configure(api_key=settings.gemini_api_key)
        _model = genai.GenerativeModel(settings.gemini_model)
    return _model


def gemini_client(prompt: str, max_retries: int = 3) -> Dict[str, Any]:
    for attempt in range(max_retries):
        try:
            chat = _get_model().start_chat(history=[])
            response = chat.send_message(prompt).text.strip()
            
            if '```' in response:
                response = response.split('```')[1].strip()
                if response.startswith('json'):
                    response = response[4:].strip()
            
            return json.loads(response)

        except (google_exceptions.InternalServerError, Exception) as e:
            if attempt < max_retries - 1:
                time.sleep(2 if isinstance(e, Exception) else 10)
                continue
            raise e
            
        except (google_exceptions.PermissionDenied, google_exceptions.ResourceExhausted, json.JSONDecodeError) as e:
            raise e

    raise Exception("Max retries exceeded")