from db import db
from models import Inventory

def load_fixtures():
    with app.app_context():
        db.create_all()
        # Add sample inventory data
        inventory_data = [
            Inventory(product_id=1, quantity=50),
            Inventory(product_id=2, quantity=100),
        ]
        db.session.bulk_save_objects(inventory_data)
        db.session.commit()
