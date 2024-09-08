from core.redis import aio_redis
from typing import Optional
from decimal import Decimal


class CachingService:
    def __init__(self):
        self.redis = aio_redis.Redis()

    async def get_product_price(self, product_reference_id: str, source: str) -> Optional[float]:
        key = f"{source}:{product_reference_id}"
        price = await self.redis.get(name=key)

        if price is None:
            return None
        return float(price)

    async def set_product_price(self, product_reference_id: str, source: str, price: Decimal) -> None:
        key = f"{source}:{product_reference_id}"
        await self.redis.set(key, str(price))

