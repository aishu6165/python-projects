import unittest
from flask_testing import TestCase
from db import db
from app import app
from models import Product

class ProductTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://product:product_password@product_db:5432/product_test'
        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_product(self):
        """Test adding a new product"""
        response = self.client.post('/products', json={
            'name': 'Monitor', 'price': 150.00, 'in_stock': 20
        })
        self.assertEqual(response.status_code, 201)

        # Check if product is added
        product = Product.query.filter_by(name='Monitor').first()
        self.assertIsNotNone(product)

    def test_get_products(self):
        """Test fetching all products"""
        # Add a product
        product = Product(name="Laptop", price=1200.00, in_stock=10)
        db.session.add(product)
        db.session.commit()

        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Laptop', response.get_data(as_text=True))

    def test_get_product(self):
        """Test fetching a single product"""
        # Add a product
        product = Product(name="Mouse", price=20.00, in_stock=100)
        db.session.add(product)
        db.session.commit()

        response = self.client.get(f'/products/{product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mouse', response.get_data(as_text=True))

    def test_get_product_not_found(self):
        """Test fetching a non-existent product"""
        response = self.client.get('/products/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('{"message":"Product not found"}', response.get_data(as_text=True))

    def test_update_product(self):
        """Test updating an existing product"""
        # Add a product
        product = Product(name="Mouse", price=20.00, in_stock=100)
        db.session.add(product)
        db.session.commit()

        response = self.client.put(f'/products/{product.id}', json={
            'name': 'Mouse', 'price': 25.00, 'in_stock': 90
        })
        self.assertEqual(response.status_code, 200)

        updated_product = Product.query.get(product.id)
        self.assertEqual(updated_product.price, 25.00)
        self.assertEqual(updated_product.in_stock, 90)

    def test_update_product_not_found(self):
        """Test updating a non-existent product"""
        response = self.client.put('/products/9999', json={
            'name': 'NonExistent', 'price': 100, 'in_stock': 5
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('{"message":"Product not found"}', response.get_data(as_text=True))

    def test_delete_product(self):
        """Test deleting a product"""
        # Add a product
        product = Product(name="Keyboard", price=45.00, in_stock=50)
        db.session.add(product)
        db.session.commit()

        response = self.client.delete(f'/products/{product.id}')
        self.assertEqual(response.status_code, 200)

        deleted_product = Product.query.get(product.id)
        self.assertIsNone(deleted_product)

    def test_delete_product_not_found(self):
        """Test deleting a non-existent product"""
        response = self.client.delete('/products/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('{"message":"Product not found"}', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
