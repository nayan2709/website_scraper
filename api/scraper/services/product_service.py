from sqlalchemy import select

from api.scraper.models.product import Product
from api.utils.cache_service import CachingService
from core import session


class ProductService:
    def __init__(self):
        pass

    @staticmethod
    async def add_or_update_product(product_data):
        query = select(Product).where(
            Product.source == product_data["source"],
            Product.product_reference_id == product_data["product_reference_id"]
        )
        result = await session.execute(query)
        products = result.scalars().all()
        if len(products) > 1:
            raise Exception("Multiple products found")
        elif len(products) == 1:
            product = products[0]
            product.sku_id = product_data["sku_id"]
            product.title = product_data["title"]
            product.price = product_data["price"]
            product.currency = product_data["currency"]
            product.path_to_image = product_data["path_to_image"]
        else:
            product = Product(
                sku_id=product_data["sku_id"],
                product_reference_id=product_data["product_reference_id"],
                title=product_data["title"],
                price=product_data["price"],
                currency=product_data["currency"],
                path_to_image=product_data["path_to_image"],
                source=product_data["source"]
            )
            session.add(product)

        return product
