from typing import Annotated

from fastapi import Depends

from app.services.product import ProductService
from app.services.price import PriceService
from app.utils.unit_of_work import AbstractUnitOfWork, UnitOfWork
from app.services.base import BaseService

UOWDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]
ProductServ = Annotated[BaseService, Depends(ProductService)]
PriceServ = Annotated[BaseService, Depends(PriceService)]
