"""
Unit Tests for Data Models
"""
import unittest
from service.models import Product, DataValidationError


class TestProductModel(unittest.TestCase):
    """Product Model Test Cases"""

    def setUp(self):
        """Runs before each test"""
        Product.remove_all()

    def tearDown(self):
        """Runs after each test"""
        Product.remove_all()

    def test_create_a_product(self):
        """It should Create a Product and assert that it exists"""
        product = Product(name="Hat", category="Apparel", available=True, price=19.99)
        self.assertTrue(product is not None)
        self.assertEqual(product.id, 0)
        self.assertEqual(product.name, "Hat")
        self.assertEqual(product.category, "Apparel")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 19.99)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name="Shoes", category="Apparel", available=True, price=59.95)
        product.create()
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should Read a Product"""
        product = Product(name="Shoes", category="Apparel", available=True, price=59.95)
        product.create()
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, "Shoes")

    def test_update_a_product(self):
        """It should Update a Product"""
        product = Product(name="Shoes", category="Apparel", available=True, price=59.95)
        product.create()
        product.price = 49.99
        product.update()
        found_product = Product.find(product.id)
        self.assertEqual(found_product.price, 49.99)

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = Product(name="Shoes", category="Apparel", available=True, price=59.95)
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_missing_key(self):
        """It should not deserialize data with missing keys"""
        data = {"name": "Hat", "price": 10.0}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)


if __name__ == "__main__":
    unittest.main()
