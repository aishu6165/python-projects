# fixtures.py
from db import db
from models import Order

def load_fixtures():
    # Sample order data
    orders = [
        {'product_id': 1, 'quantity': 2},
        {'product_id': 2, 'quantity': 1},
    ]
    for order_data in orders:
        order = Order(**order_data)
        db.session.add(order)
    db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        load_fixtures()
