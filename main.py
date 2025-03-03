import uvicorn
import logging.config
from app import app


if __name__ == "__main__":
    uvicorn.run("app:app", log_level="info", reload=True)