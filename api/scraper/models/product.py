from sqlalchemy import Column, String, Float, Index, Integer
from core.session import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku_id = Column(String, nullable=False)
    product_reference_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    path_to_image = Column(String, nullable=False)
    source = Column(String, nullable=False)

    __table_args__ = (
        Index("idx_products_source_source_id", "source", "product_reference_id"),
    )
