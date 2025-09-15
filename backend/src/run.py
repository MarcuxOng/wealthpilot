import uvicorn
from dotenv import load_dotenv
from src.config import settings

load_dotenv()

if __name__ == '__main__':
    from src.main import app

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
        log_level="info"
    )