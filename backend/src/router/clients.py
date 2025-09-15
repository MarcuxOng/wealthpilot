from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.database.models import Client

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("")
def get_all_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients
