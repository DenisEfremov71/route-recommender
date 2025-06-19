from pydantic import BaseModel
from typing import List

class Store(BaseModel):
    retailer: str
    store_number: str
    address: str

class StoreList(BaseModel):
    stores: List[Store] 