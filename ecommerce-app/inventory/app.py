from flask import Flask, request, jsonify
import redis
import json
from db import db
from models import Inventory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://inventory:inventory_password@inventory_db:5432/inventory'
redis_client = redis.Redis(host='redis', port=6379, password='RedisPasswordSecret')
db.init_app(app)
db.app = app
app.db = db
with app.app_context():
    db.create_all()
@app.route('/inventory/<int:product_id>', methods=['GET'])
def get_inventory(product_id):
    inventory = Inventory.query.filter_by(product_id=product_id).first()
    if not inventory:
        return jsonify({'message': 'Inventory not found'}), 404
    return jsonify({'product_id': inventory.product_id, 'quantity': inventory.quantity})
    
@app.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']
    # Check if inventory item for the product already exists
    inventory_item = Inventory.query.filter_by(product_id=product_id).first()
    
    if inventory_item:
        # If product exists, update the quantity
        inventory_item.quantity += quantity  # Increment the quantity
        db.session.commit()
        event_data = {'product_id': product_id, 'quantity': inventory_item.quantity,'event_type': 'update_stock'}
        redis_client.publish('inventory_events', json.dumps(event_data))
        return jsonify({'message': 'Inventory updated successfully', 'product_id': inventory_item.product_id, 'new_quantity': inventory_item.quantity}), 200
    else:
        # If product does not exist, add new inventory item
        new_inventory = Inventory(product_id=product_id, quantity=quantity)
        db.session.add(new_inventory)
        db.session.commit()
        # Publish an event to Redis
        redis_client.publish('inventory_events', json.dumps({
            'product_id': new_inventory.product_id,
            'quantity': new_inventory.quantity,
            'event_type': 'update_stock'
        }))
        event_data = {'product_id': new_inventory.product_id, 'quantity': new_inventory.quantity,'event_type': 'update_stock'}
        redis_client.publish('inventory_events', json.dumps(event_data))
        return jsonify({'message': 'Inventory added successfully', 'product_id': new_inventory.product_id, 'quantity': new_inventory.quantity}), 201

def handle_order_event(message):
    order_data = json.loads(message['data'])
    product_id = order_data['product_id']
    quantity = order_data['quantity']

    # Reduce the inventory
    inventory_item = Inventory.query.filter_by(product_id=product_id).first()
    if inventory_item and inventory_item.quantity >= quantity:
        inventory_item.quantity -= quantity
        db.session.commit()
        # Publish an event to update product
        redis_client.publish('inventory_events', json.dumps({
            'product_id': product_id,
            'quantity': quantity,
            'event_type': 'reduce_stock'
        }))
        return True
    return False

def listen_to_order_events():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('order_events')
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_order_event(message)

if __name__ == '__main__':
    import threading
    threading.Thread(target=listen_to_order_events).start()
    app.run(host='0.0.0.0', port=5006)
