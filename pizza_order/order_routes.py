from fastapi import APIRouter, status, Depends, HTTPException
from models import User, Order
from pizza_order.schemas import OrderRequestModel, OrderOut, OrderUpdate
from user.dependencies import get_current_user, get_db
from sqlalchemy.orm import Session
from typing import List


order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@order_router.get('/')
async def hello():
    return {"message":"Hello! These route you order a pizza."}


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_order(order:OrderRequestModel, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
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


@order_router.get('/orders', response_model=List[OrderOut])
async def list_orders(current_user:User = Depends(get_current_user), db: Session = Depends(get_db)):
      user = db.query(User).filter(User.username == current_user.username).first()

      if user.is_staff:
            orders = db.query(Order).all()
            return orders
      
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="User not allowed to access this information.")


@order_router.get('/orders/{id}', response_model=OrderOut)
async def get_order_by_id(id:int, current_user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user.username).first()

    if user.is_staff:
        order = db.query(Order).filter(Order.id == id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
        return order
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not allowed to access this information.")


@order_router.get('/user/orders', response_model=List[OrderOut])
async def get_user_orders(current_user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.orders


@order_router.get('/user/order/{id}', response_model=OrderOut)
async def get_user_order(id:int, current_user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    orders = user.orders

    for order in orders:
         if order.id == id:
              return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No order with such id.")


@order_router.put('/order/update/{id}', response_model=OrderOut)
async def update_order(id: int, order: OrderUpdate, current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    order_update = db.query(Order).filter(Order.id == id).first()

    if not order_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")

    if not current_user.is_staff and order_update.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not allowed to update this order.")

    update_data = order.model_dump(exclude_unset=True)  # Ignora campos não enviados (útil se for PATCH também)

    if "pizza_size" in update_data:
        update_data["pizza_size"] = update_data["pizza_size"].value.lower()

    if "order_status" in update_data:
        update_data["order_status"] = update_data["order_status"].value.lower()

    for field, value in update_data.items():
        setattr(order_update, field, value)

    db.commit()
    db.refresh(order_update)
    return order_update


@order_router.delete('/order/delete/{id}', response_model=OrderOut, status_code=status.HTTP_200_OK)
async def delete_order(id: int, current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    order_delete = db.query(Order).filter(Order.id == id).first()

    if not order_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")

    if not current_user.is_staff and order_delete.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not allowed to delete this order.")

    db.delete(order_delete)
    db.commit()

    return order_delete