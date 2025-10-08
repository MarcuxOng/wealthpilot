from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.database.models import AnalyseHistory, Client

router = APIRouter(prefix="/analysis_history", tags=["Analysis History"])

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