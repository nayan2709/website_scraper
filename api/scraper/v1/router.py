from fastapi import APIRouter

from api.scraper.v1.scraper import scraper_router

router = APIRouter()
router.include_router(scraper_router, tags=["scraper"])