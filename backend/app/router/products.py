from fastapi import APIRouter
from app.load_data.data import product_data

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("")
def get_all_products():
    return product_data