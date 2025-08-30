from fastapi import APIRouter
from app.load_data.data import client_data

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/")
def get_all_clients():
    return client_data
