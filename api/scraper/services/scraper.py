import asyncio
import os
import logging
import re

import httpx
from bs4 import BeautifulSoup
import requests

from api.scraper.services.notification import Notification
from api.scraper.services.product_service import ProductService
from api.utils.cache_service import CachingService
from core import Transactional
from core.config import config

logger = logging.getLogger(__name__)


class ScraperService:
    def __init__(self, page_limit=1, proxy=""):
        self.proxy = proxy
        self.page_limit = page_limit
        self.product_service = ProductService()
        self.caching_service = CachingService()
        self.notification = Notification()

    @Transactional()
    async def process_products(self, products):
        new_or_updated_products = []
        for product in products:
            price = await self.caching_service.get_product_price(
                product["product_reference_id"],
                product["source"]
            )
            if price is not None and price == product["price"]:
                continue
            await self.product_service.add_or_update_product(product)
            await self.caching_service.set_product_price(
                product["product_reference_id"],
                product["source"],
                product["price"]
            )
            new_or_updated_products.append(product["product_reference_id"])

        return new_or_updated_products

    async def scrape_website(self):
        logger.info("Scraping started")
        final_response = {}
        products = []
        page = 1
        try:
            while True:
                url = f"{config.BASE_URL}"
                if page != 1:
                    url = f"{url}/page/{page}/"
                response = await self._get_page(url)
                if response is None:
                    break
                soup = BeautifulSoup(response, "html.parser")
                product_elements = soup.find_all('li', class_='product')
                logger.info(f"Page number {page} - {len(product_elements)} products found!")
                for element in product_elements:
                    title = element.find('h2', class_='woo-loop-product__title').find('a')['href'].split('/')[-2]
                    price_str = element.find('span', class_='woocommerce-Price-amount').text.strip()
                    image_url = element.find('img', class_='attachment-woocommerce_thumbnail')['src']
                    if '.jpg' not in image_url:
                        image_url = element.find('img', class_='attachment-woocommerce_thumbnail')['data-lazy-src']
                    currency, price = self.extract_price_and_currency(price_str)
                    products.append(
                        {
                            "sku_id": element.find('a', class_='button').get('data-product_sku', ''),
                            "product_reference_id": element.find('a', class_='button').get('data-product_sku', ''),
                            "title": title,
                            "price": price,
                            "currency": currency,
                            "path_to_image": await self._download_image(image_url),
                            "source": url
                        }
                    )
                if page >= self.page_limit:
                    break
                page += 1
            logger.info(f'total products: {len(products)}')

            new_or_updated_products = []
            batch_size = 10
            for i in range(0, len(products), batch_size):
                batch = products[i:i + batch_size]
                new_or_updated_products.extend(await self.process_products(batch))
            final_response = {
                "total_products_scraped": len(products),
                "total_products_upserted": len(new_or_updated_products)
            }
            self.notification.notify(final_response)
        except Exception as e:
            logger.error(e)
            pass
        finally:
            return final_response

    async def _get_page(self, url):
        retries = config.REQUEST_RETRIES
        for _ in range(retries):
            try:
                response = requests.get(
                    url,
                    proxies={
                        "http": self.proxy,
                        "https": self.proxy
                    } if self.proxy else None
                )
                if response.status_code == 200:
                    return response.text
            except requests.RequestException:
                await asyncio.sleep(2)
        return None

    async def _download_image(self, url: str) -> str:
        file_path = f"data/images/{os.path.basename(url)}.jpg"
        if os.path.exists(file_path):
            return file_path

        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                return file_path
            return ""

    @staticmethod
    def extract_price_and_currency(text: str):
        # The pattern captures currency symbols and floating-point numbers
        pattern = re.compile(r'(?P<currency>[₹$€£¥])\s*(?P<amount>\d+(?:\.\d{1,2})?)')
        match = pattern.search(text)

        if match:
            currency = match.group('currency')
            amount = match.group('amount')
            return currency, float(amount)

        return None, None