from fastapi import APIRouter

from app.data.data import db_data
from app.llm.gemini import gemini_client
from app.llm.sysPrompt import system_prompt

router = APIRouter(prefix="/client", tags=["Client Analysis"])


@router.get("/{client_id}")
def get_client_analysis(client_id: str):
    client = db_data["clients"].get(client_id)
    if not client:
        return {"error": f"Client {client_id} not found"}

    print(f"Analysing Client ID: {client_id}")
    prompt = system_prompt(client, db_data["products"])
    ai_analysis = gemini_client(prompt)

    if "error" in ai_analysis:
        return {
            "client": client,
            "ai_analysis": ai_analysis,
            "status": "error"
        }

    return {
        "client": client,
        "ai_analysis": ai_analysis,
        "status": "success"
    }