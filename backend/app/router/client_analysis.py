from fastapi import APIRouter

from app.load_data.data import client_data, product_data
from app.llm.gemini import gemini_client
from app.llm.sysPrompt import system_prompt
from app.storage.analysis_storage import analysis_storage

router = APIRouter(prefix="/client_analysis", tags=["Client Analysis"])


@router.get("/{client_id}")
def get_client_analysis(client_id: str):
    client = client_data.get(client_id)
    products = product_data
    if not client:
        return {"error": f"Client {client_id} not found"}

    print(f"INFO:     Analysing Client ID: {client_id}")
    prompt = system_prompt(client, products)
    ai_analysis = gemini_client(prompt)

    if "error" in ai_analysis:
        return {
            "client": client,
            "ai_analysis": ai_analysis,
            "status": "error"
        }

    # Store the successful AI analysis
    analysis_data = {
        "client": client,
        "ai_analysis": ai_analysis,
        "status": "success"
    }
    
    # Store the analysis data
    storage_success = analysis_storage.store_analysis(client_id, analysis_data)
    if not storage_success:
        print(f"Warning: Failed to store analysis for client {client_id}")

    return analysis_data


@router.get("/history/all")
def get_all_analysis_history():
    all_analyses = analysis_storage.get_all_analyses()
    
    return {
        "total_analyses": len(all_analyses),
        "analyses": all_analyses
    }


@router.delete("/{client_id}/history/{timestamp}")
def delete_specific_analysis(client_id: str, timestamp: str):
    success = analysis_storage.delete_specific_analysis(client_id, timestamp)
    
    if success:
        return {"message": f"Specific analysis for client {client_id} deleted successfully"}
    else:
        return {"error": f"No analysis found for client {client_id} with timestamp {timestamp}"}