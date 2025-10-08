from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.router import clients, client_analysis, products, analysis_history


app = FastAPI(
    title="HSBC Wealth Management AI API",
    description="AI-powered client analysis and product recommendations",
    version="1.0.0"
)

origins = [settings.origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client_analysis.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(analysis_history.router)

@app.get("/", tags=["Root"])
def read_root():
    return "HSBC Wealth Management AI API"