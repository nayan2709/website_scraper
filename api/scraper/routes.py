from fastapi import APIRouter

from api.scraper.v1.scraper import scraper_router as scraper_router_v1

scrape_router = APIRouter()
scrape_router.include_router(scraper_router_v1, prefix="/v1", tags=["scraper"])

