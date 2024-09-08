import uvicorn
import logging

from fastapi import FastAPI

from api import router
from core.config import config
from core.fastapi.middlewares import SQLAlchemyMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(SQLAlchemyMiddleware)
]

app = FastAPI(middleware=middleware)
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    logging.info("Starting Uvicorn server")
    uvicorn.run(
        app,
        host=config.APP_HOST,
        port=config.APP_PORT,
    )
