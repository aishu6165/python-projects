from db import db
from sqlalchemy import Column, Integer, Float, String

class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    price = Column(Float())
    in_stock = Column(Integer())
