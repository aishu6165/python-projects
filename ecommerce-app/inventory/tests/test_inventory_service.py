import unittest
from unittest.mock import patch
from app import app, db, Inventory, listen_to_order_events  # Import the function

class InventoryServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.execute('TRUNCATE TABLE inventory CASCADE;')
            db.session.commit()

    def test_add_inventory(self):
        response = self.client.post('/inventory', json={'product_id': 1, 'quantity': 100})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"message":"Inventory added successfully","product_id":1,"quantity":100}', response.data)

    def test_get_inventory(self):
        self.client.post('/inventory', json={'product_id': 1, 'quantity': 100})
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"product_id": 1, "quantity": 100})  # Updated assertion

    def test_get_inventory_not_found(self):
        response = self.client.get('/inventory/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'{"message":"Inventory not found"}', response.data)

    @patch('app.redis_client')
    def test_handle_order_event_updates_inventory(self, mock_redis):
        self.client.post('/inventory', json={'product_id': 1, 'quantity': 100})
        mock_redis.pubsub.return_value.listen.return_value = [
            {'type': 'message', 'data': '{"product_id": 1, "quantity": 10}'}
        ]

        listen_to_order_events()  # Call the function directly
        inventory = Inventory.query.filter_by(product_id=1).first()
        self.assertEqual(inventory.quantity, 90)

    @patch('app.redis_client')
    def test_handle_order_event_insufficient_inventory(self, mock_redis):
        self.client.post('/inventory', json={'product_id': 1, 'quantity': 5})
        mock_redis.pubsub.return_value.listen.return_value = [
            {'type': 'message', 'data': '{"product_id": 1, "quantity": 10}'}
        ]

        listen_to_order_events()  # Call the function directly
        inventory = Inventory.query.filter_by(product_id=1).first()
        self.assertEqual(inventory.quantity, 5)  # Should not change

if __name__ == '__main__':
    unittest.main()
