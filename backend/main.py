import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.gemini import gemini_client
from backend.sysPrompt import system_prompt
from backend.config import settings


def load_data():
    data_file_path = os.path.join(os.path.dirname(__file__), "data", "data.json")
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file_path}")
        return {"clients": {}, "products": {}}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in data file: {e}")
        return {"clients": {}, "products": {}}


def main() -> FastAPI:
    app = FastAPI(
        title="HSBC Wealth Management AI API",
        description="AI-powered client analysis and product recommendations",
        version="1.0.0"
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load data from JSON file
    db_data = load_data()

    @app.get("/", tags=["Root"])
    def read_root():
        return "HSBC Wealth Management AI API"

    @app.get("/client/{client_id}", tags=["Client Analysis"])
    def get_client_analysis(client_id: str):
        client = db_data["clients"].get(client_id)
        if not client:
            return {"error": f"Client {client_id} not found"}

        print(f"Analyzing client: {client['name']} (ID: {client_id})")

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

    @app.get("/products", tags=["Products"])
    def get_all_products():
        return db_data["products"]

    @app.get("/test-simple", tags=["Testing"])
    def test_simple():
        """Simple test endpoint to verify API is working"""
        return {
            "message": "API is working correctly",
            "status": "ok",
            "available_clients": list(db_data["clients"].keys()),
            "available_products": len(db_data["products"])
        }

    return app


app = main()