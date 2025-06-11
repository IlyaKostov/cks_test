from pydantic import BaseModel, ConfigDict


class ProductSchema(BaseModel):
    id: int
    url: str
    name: str | None
    description: str | None
    rating: float | None

    model_config = ConfigDict(from_attributes=True)


class ProductWithPriceSchema(ProductSchema):
    price: float | None
