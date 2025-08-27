from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.data.data import load_data
from backend.llm.gemini import gemini_client
from backend.llm.sysPrompt import system_prompt


def main() -> FastAPI:
    app = FastAPI(
        title="HSBC Wealth Management AI API",
        description="AI-powered client analysis and product recommendations",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
        return {
            "message": "API is working correctly",
            "status": "ok",
            "available_clients": list(db_data["clients"].keys()),
            "available_products": len(db_data["products"])
        }

    return app


app = main()