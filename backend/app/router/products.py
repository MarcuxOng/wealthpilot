from fastapi import APIRouter
from app.data.data import db_data

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_all_products():
    return db_data["products"]