from fastapi import APIRouter

from api.scraper.routes import scrape_router

router = APIRouter()

router.include_router(scrape_router, tags=["scraper"])
