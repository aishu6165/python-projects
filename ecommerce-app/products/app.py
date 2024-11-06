
from flask import Flask, request, jsonify, abort
from db import db
from models import Product
import redis
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://product:product_password@product_db:5432/product'
db.init_app(app)
db.app = app
app.db = db
with app.app_context():
    db.create_all()
redis_client = redis.Redis(host='redis', port=6379, password='RedisPasswordSecret')

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({"message": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"message": "Bad request: invalid input"}), 400

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'in_stock': p.in_stock} for p in products])

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'in_stock': product.in_stock})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    try:
        new_product = Product(name=data['name'], price=float(data['price']), in_stock=int(data['in_stock']))
    except (KeyError, ValueError):
        abort(400)  # Input validation failed
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    try:
        product.name = data['name']
        product.price = float(data['price'])
        product.in_stock = int(data['in_stock'])
    except (KeyError, ValueError):
        abort(400)  # Input validation failed
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

def handle_inventory_event(message):
    inventory_data = json.loads(message['data'])
    event_type = inventory_data.get('event_type')
    product_id = inventory_data['product_id']
    quantity = inventory_data['quantity']
    product = Product.query.get(product_id)
    if event_type == 'reduce_stock' and product:
        # Handle stock reduction event
        product.in_stock -= quantity
        db.session.commit()
        print(f"Product {product_id} stock reduced by {quantity}")
    elif event_type == 'update_stock' and product:
        # Handle inventory update event
        product.in_stock = quantity
        db.session.commit()
        print(f"Product {product_id} stock updated to {quantity}")

def listen_to_inventory_events():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('inventory_events', 'inventory_update_event')
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_inventory_event(message)

if __name__ == '__main__':
    import threading
    threading.Thread(target=listen_to_inventory_events).start()
    app.run(host='0.0.0.0', port=5005)
