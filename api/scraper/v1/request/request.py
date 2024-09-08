from typing import Optional

from pydantic import BaseModel


class ScraperRequest(BaseModel):
    page_limit: Optional[int] = 1
    proxy: Optional[str] = ""
