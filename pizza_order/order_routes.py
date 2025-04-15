from fastapi import APIRouter, status, Depends
from models import User, Order
from pizza_order.schemas import OrderModel
from user.dependencies import get_current_user, get_db
from sqlalchemy.orm import Session


order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@order_router.get('/')
async def hello():
    return {"message":"Hello! These route you order a pizza."}


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_order(order:OrderModel, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
        new_order = Order(pizza_size = order.pizza_size, quantity = order.quantity,
                      flavour = order.flavour, user = current_user)
    
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        response = {
            "id":new_order.id,
            "pizza_size":new_order.pizza_size,
            "quantity":new_order.quantity,
            "order_status":new_order.order_status,
            "flavour":new_order.flavour
        }

        return response