import uvicorn
from dotenv import load_dotenv
from app.config import settings

load_dotenv()

if __name__ == '__main__':
    from app.main import app

    uvicorn.run(
        "backend.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
        log_level="info"
    )