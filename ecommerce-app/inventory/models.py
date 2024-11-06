from db import db
from sqlalchemy import Column, Integer

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), nullable=False)
    quantity = Column(Integer(), nullable=False)
