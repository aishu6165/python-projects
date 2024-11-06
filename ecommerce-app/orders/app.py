import requests
from flask import Flask, request, jsonify
from models import db, Order
import redis
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://order:order_password@order_db:5432/order'
redis_client = redis.Redis(host='redis', port=6379, password='RedisPasswordSecret')
db.init_app(app)
with app.app_context():
    db.create_all()


def get_product(product_id):
    """Check if product exists in the products service"""
    try:
        response = requests.get(f'http://product-service:5005/products/{product_id}')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error contacting product service: {e}")
        return None

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']

    # Check if the product exists
    product = get_product(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Check inventory before creating an order
    try:
        inventory_response = requests.get(f'http://inventory-service:5006/inventory/{product_id}')
        if inventory_response.status_code != 200:
            return jsonify({'message': 'Inventory service not available'}), 503

        inventory = inventory_response.json()
        if inventory['quantity'] <= 0:
            return jsonify({'message': 'Product is sold out'}), 400  # Notify sold out

        if inventory['quantity'] < quantity:
            return jsonify({'message': 'Not enough inventory available'}), 400  # Notify insufficient inventory
    except Exception as e:
        print(f"Error checking inventory: {e}")
        return jsonify({'message': 'Error checking inventory'}), 500
    
    final_price = int(product['price']) * int(data['quantity'])
    new_order = Order(product_id=data['product_id'], quantity=data['quantity'], total_price=final_price)
    db.session.add(new_order)
    db.session.commit()
    
    # Publish an event to update inventory
    redis_client.publish('order_events', json.dumps({
        'product_id': new_order.product_id,
        'quantity': new_order.quantity
    }))
    return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201


@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    return jsonify({'id': order.id, 'product_id': order.product_id, 'quantity': order.quantity, 'total_price': order.total_price})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)