from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import clients, client_analysis, products


app = FastAPI(
    title="HSBC Wealth Management AI API",
    description="AI-powered client analysis and product recommendations",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return "HSBC Wealth Management AI API"

app.include_router(client_analysis.router)
app.include_router(clients.router)
app.include_router(products.router)