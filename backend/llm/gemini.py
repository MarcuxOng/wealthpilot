import json
import time
from typing import Dict, Any
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from backend.config import settings

# Configure Gemini with settings from config
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel(settings.gemini_model)


def gemini_client(prompt: str, max_retries: int = 3) -> Dict[str, Any]:
    """
    Send prompt to Gemini API with retry logic and comprehensive error handling
    """
    for attempt in range(max_retries):
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            raw_response = response.text.strip()
            cleaned_response = raw_response

            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response.split('```json')[1].split('```')[0].strip()
            elif cleaned_response.startswith('```'):
                cleaned_response = cleaned_response.split('```')[1].split('```')[0].strip()

            parsed_response = json.loads(cleaned_response)
            return parsed_response

        except google_exceptions.InternalServerError as e:
            if attempt < max_retries - 1:
                print(f"Gemini API internal server error (attempt {attempt + 1}/{max_retries}). Retrying in 2 seconds...")
                time.sleep(2)
                continue
            else:
                return {
                    "error": "Gemini API is experiencing temporary issues. Please try again later.",
                    "details": str(e),
                    "status": "api_error"
                }
                
        except google_exceptions.InvalidArgument as e:
            return {
                "error": "Invalid request to Gemini API",
                "details": str(e),
                "status": "invalid_request"
            }
            
        except google_exceptions.PermissionDenied as e:
            return {
                "error": "API key is invalid or doesn't have permission to access Gemini",
                "details": str(e),
                "status": "permission_denied"
            }
            
        except google_exceptions.ResourceExhausted as e:
            return {
                "error": "API quota exceeded. Please try again later.",
                "details": str(e),
                "status": "quota_exceeded"
            }
            
        except json.JSONDecodeError as e:
            return {
                "error": "Failed to parse Gemini API response",
                "details": f"JSON decode error: {str(e)}",
                "raw_response": raw_response[:500] + "..." if len(raw_response) > 500 else raw_response,
                "status": "parse_error"
            }
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}. Retrying in 2 seconds...")
                time.sleep(2)
                continue
            else:
                return {
                    "error": "An unexpected error occurred while processing your request",
                    "details": str(e),
                    "status": "unknown_error"
                }
    
    return {
        "error": "Failed to get response from Gemini API after multiple attempts",
        "status": "max_retries_exceeded"
    }