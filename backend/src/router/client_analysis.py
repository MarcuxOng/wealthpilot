from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.database.models import AnalyseHistory, Client, Product
from src.llm.gemini import gemini_client
from src.llm.sysPrompt import system_prompt

router = APIRouter(prefix="/client_analysis", tags=["Client Analysis"])


@router.get("/{client_id}")
def get_client_analysis(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

    products = db.query(Product).all()
    if not products:
        # You might want to seed your products table first
        raise HTTPException(status_code=404, detail="No products found in the database")

    print(f"INFO:     Analysing Client ID: {client_id}")
    prompt = system_prompt(client, products)
    ai_analysis = gemini_client(prompt)

    if "error" in ai_analysis:
        return {
            "client": client.__dict__,
            "ai_analysis": ai_analysis,
            "status": "error"
        }

    # Store the analysis data
    new_analysis_record = AnalyseHistory(
        client_id=client.id,
        analysis_result=ai_analysis
    )
    db.add(new_analysis_record)
    db.commit()
    db.refresh(new_analysis_record)

    return {
        "client": client.__dict__,
        "ai_analysis": ai_analysis,
        "status": "success"
    }


@router.get("/history/all")
def get_all_analysis_history(db: Session = Depends(get_db)):
    results = db.query(AnalyseHistory, Client).join(Client, AnalyseHistory.client_id == Client.id).all()

    analyses_with_client_data = []
    for analysis, client in results:
        analyses_with_client_data.append({
            "id": analysis.id,
            "client_id": analysis.client_id,
            "client_name": client.name,
            "analysis_result": analysis.analysis_result,
        })

    return {
        "total_analyses": len(analyses_with_client_data),
        "analyses": analyses_with_client_data
    }


@router.get("/history/{client_id}")
def get_client_analysis_history(client_id: str, db: Session = Depends(get_db)):
    history = db.query(AnalyseHistory).filter(AnalyseHistory.client_id == client_id).all()
    return history