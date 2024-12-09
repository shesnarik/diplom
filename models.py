from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True)
    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_name = Column(String)
    delivery_time = Column(DateTime)
    status = Column(String)  # e.g., 'pending', 'completed', 'cancelled'

    user = relationship("User", back_populates="orders")