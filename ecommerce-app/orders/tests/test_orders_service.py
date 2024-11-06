#work in progress
# import unittest
# from flask_testing import TestCase
# from app import app, db
# from models import Order  # Assuming you have an Order model defined

# class OrderTestCase(TestCase):

#     def create_app(self):
#         app.config['TESTING'] = True
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://order:order_password@order_db:5432/order_test'
#         return app

#     def setUp(self):
#         with self.app.app_context():
#             db.create_all()

#     def tearDown(self):
#         with self.app.app_context():
#             db.session.remove()
#             db.drop_all()

#     def test_create_order(self):
#         """Test creating a new order"""
#         # Here we assume that there is a product with id 1 in the database
#         response = self.client.post('/orders', json={
#             'product_id': 1,
#             'quantity': 2
#         })
#         self.assertEqual(response.status_code, 201)
#         self.assertIn(b'Order created successfully', response.data)

#     def test_create_order_with_nonexistent_product(self):
#         """Test creating an order with a nonexistent product"""
#         response = self.client.post('/orders', json={
#             'product_id': 999,  # Assuming this product does not exist
#             'quantity': 1
#         })
#         self.assertEqual(response.status_code, 404)
#         self.assertIn(b'Product not found', response.data)

# if __name__ == '__main__':
#     unittest.main()
