from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from api.scraper.services.scraper import ScraperService
from api.scraper.v1.request.request import ScraperRequest
from core.fastapi.dependencies.dependency import IsAuthenticated

scraper_router = APIRouter()


@scraper_router.get("/scrape", dependencies=[Depends(IsAuthenticated())])
async def scrape_website(scraper_request: ScraperRequest):
    data = await ScraperService(
        page_limit=scraper_request.page_limit,
        proxy=scraper_request.proxy
    ).scrape_website()
    return JSONResponse(status_code=200, content=data)
