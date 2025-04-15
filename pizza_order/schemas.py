from pydantic import BaseModel
from typing import Optional


class OrderModel(BaseModel):
    quantity:int
    order_status:Optional[str] = "PENDING"
    pizza_size:Optional[str] = "SMALL"
    flavour:str


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example":{
                "quantity":1,
                "order_status":"DELIVERED",
                "pizza_size":"LARGE",
                "flavour":"Mozzarella"
            }
        }