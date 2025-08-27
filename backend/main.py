from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from backend.gemini import gemini_client

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
fake_db = {
    "clients": {
        "123": {
            "id": "123",
            "name": "John Doe",
            "risk_profile": "moderate",
            "existing_products": ["Savings Account", "Investment Portfolio"]
        }
    },
    "products": {
        "1": {"id": "1", "name": "Retirement Fund", "risk_level": "low"},
        "2": {"id": "2", "name": "Growth Stocks", "risk_level": "high"}
    }
}

class Client(BaseModel):
    id: str
    name: str
    risk_profile: str
    existing_products: List[str]

class Product(BaseModel):
    id: str
    name: str
    risk_level: str

@app.get("/")
def read_root():
    return {"message": "Wealth Management API"}

@app.get("/client/{client_id}", response_model=Dict)
def get_client_data(client_id: str):
    client = fake_db["clients"].get(client_id)
    if not client:
        return {"error": "Client not found"}
    
    # Placeholder for AI recommendations
    recommendations = generate_recommendations(client)
    
    return {
        "client": client,
        "recommendations": recommendations
    }

@app.get("/products", response_model=Dict[str, Product])
def get_all_products():
    return fake_db["products"]

from backend.gemini import gemini_client
import json

def generate_recommendations(client: Dict) -> List[Dict]:
    # Format client data for Gemini
    client_data = f"""
    Client Profile:
    - ID: {client['id']}
    - Name: {client['name']}
    - Risk Profile: {client['risk_profile']}
    - Current Products: {', '.join(client['existing_products'])}
    """
    
    try:
        # Get AI analysis and parse JSON response
        analysis = gemini_client(client_data)
        return json.loads(analysis)
    except Exception as e:
        print(f"AI analysis failed: {str(e)}")
        return []