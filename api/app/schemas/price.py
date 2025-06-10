from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PriceBase(BaseModel):
    price: float


class PriceSchema(PriceBase):
    id: int
    product_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
