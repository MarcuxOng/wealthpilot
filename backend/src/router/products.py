from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.database.models import Product

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {"products": products}