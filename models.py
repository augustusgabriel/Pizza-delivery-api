from postgres.database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, Enum as SqlEnum
import enum
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='user'
    id=Column(Integer, primary_key=True)
    username=Column(String(40), unique=True)
    email=Column(String(80), unique=True)
    password=Column(Text, nullable=True)
    is_staff=Column(Boolean, default=False)
    is_active=Column(Boolean, default=False)
    orders=relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}"


class Order(Base):

    class OrderStatus(enum.Enum):
        pending = "pending"
        in_transit = "in_transit"
        delivered = "delivered"
    
    class PizzaSizes(enum.Enum):
        small =  "small"
        medium = "medium"
        large = "large"
        extra_large = "extra-large"
    

    __tablename__='orders'
    id=Column(Integer, primary_key=True)
    quantity=Column(Integer, nullable=False)
    order_status=Column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.pending)
    pizza_size=Column(SqlEnum(PizzaSizes), nullable=False, default=PizzaSizes.small)
    flavour=Column(String)
    user_id=Column(Integer, ForeignKey('user.id'))
    user=relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id}"
    
    @property
    def pizza_size_str(self):
        return self.pizza_size.value if self.pizza_size else None

    @property
    def order_status_str(self):
        return self.order_status.value if self.order_status else None