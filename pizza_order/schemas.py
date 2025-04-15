from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum


class OrderStatusEnum(str, Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"


class PizzaSizesEnum(str, Enum):
    small =  "small"
    medium = "medium"
    large = "large"
    extra_large = "extra-large"

class OrderRequestModel(BaseModel):
    quantity: int
    order_status: Optional[OrderStatusEnum] = OrderStatusEnum.pending.value
    pizza_size: Optional[PizzaSizesEnum] = PizzaSizesEnum.small.value
    flavour: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 1,
                "order_status": "delivered",
                "pizza_size": "large",
                "flavour": "Mozzarella"
            }
        }


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class OrderResponseModel(BaseModel):
    id: int
    quantity: int
    order_status: str
    pizza_size: str
    flavour: str
    user_id: int

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    pizza_size_str: str
    quantity: int
    order_status_str: str
    flavour: str
    user: UserOut

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    quantity: Optional[int]
    pizza_size: Optional[PizzaSizesEnum]
    flavour: Optional[str]
    order_status: Optional[OrderStatusEnum]

    @field_validator('pizza_size', mode='before')
    @classmethod
    def normalize_pizza_size(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value

    @field_validator('order_status', mode='before')
    def normalize_status(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value