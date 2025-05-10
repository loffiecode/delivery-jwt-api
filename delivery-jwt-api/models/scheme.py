from sqlalchemy import Column, Integer, String, \
        ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

from datetime import datetime


DB = declarative_base()

class Order(DB):
    __tablename__ = 'orders'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Description = Column(String, nullable=True)
    Name = Column(String, nullable=False)
    PickUpAddress = Column(String, nullable=False)
    DeliveryAddress = Column(String, nullable=False)
    Weight = Column(Integer, nullable=False)
    Dimensions = Column(String, nullable=False)
    CreationDate = Column(DateTime, default=datetime.now)

    delivery = relationship(
        'Delivery', 
        back_populates='order', 
        cascade='all, delete-orphan', 
        uselist=False
    )

class Delivery(DB):
    __tablename__ = 'deliveries'
    
    DeliveryID = Column(Integer, primary_key=True, autoincrement=True)
    ID = Column(Integer, ForeignKey('orders.ID', ondelete='CASCADE'), unique=True, nullable=False)
    Status = Column(String, default="created delivery request")
    TargetTimeDelivery = Column(DateTime, nullable = True)

    order = relationship('Order', back_populates='delivery')

class User(DB):
    __tablename__ = "users"

    ID = Column(Integer, primary_key=True)
    Username = Column(String(32), unique=True)
    Salt = Column(String(64))
    Password = Column(String(256))