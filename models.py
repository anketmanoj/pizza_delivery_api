
from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, Text, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = "now()")
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    orders = relationship("Orders", back_populates="users")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Orders(Base):

    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered'),
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('XLARGE', 'xlarge'),
    )

    __tablename__ = "orders"
    id = Column(Integer, primary_key = True, nullable=False)
    quantity = Column(Integer, nullable = False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), nullable=False, server_default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), nullable=False, server_default="SMALL")
    flavour = Column(String, nullable=False, server_default="pepperoni")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    user = relationship("Users", back_populates="orders")

    def __repr__(self) -> str:
        return f"<Order {self.id}>"