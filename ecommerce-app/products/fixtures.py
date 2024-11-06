from db import db
from models import Product

def load_fixtures():
    products = [
        {'name': 'Laptop', 'price': 1200.00, 'in_stock': 10},
        {'name': 'Mouse', 'price': 25.00, 'in_stock': 100},
        {'name': 'Keyboard', 'price': 45.00, 'in_stock': 50},
    ]
    for product_data in products:
        # Check if the product already exists by name
        existing_product = Product.query.filter_by(name=product_data['name']).first()
        if existing_product:
            # Update the existing product's attributes
            existing_product.price = product_data['price']
            existing_product.in_stock = product_data['in_stock']
        else:
            # Add new product if it doesn't exist
            new_product = Product(**product_data)
            db.session.add(new_product)

    db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        load_fixtures()