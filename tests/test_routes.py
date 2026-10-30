"""
Test cases for Product Service Routes
"""
import unittest
from service import app
from service.models import Product
from service.common import status

BASE_URL = "/products"


class TestProductServer(unittest.TestCase):
    """Product Service Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        Product.remove_all()

    def tearDown(self):
        """Runs after each test"""
        Product.remove_all()

    def test_index(self):
        """It should return the index page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "SERVICERUNNING")
        self.assertEqual(data["port"], 8000)

    def test_health(self):
        """It should return health status OK"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_get_product_list(self):
        """It should Get a list of Products"""
        product = Product(name="Shirt", category="Apparel", available=True, price=25.0)
        product.create()
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)

    def test_get_product(self):
        """It should Get a single Product"""
        product = Product(name="Pants", category="Apparel", available=True, price=45.0)
        product.create()
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Pants")

    def test_get_product_not_found(self):
        """It should not Get a Product that is not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        """It should Create a new Product"""
        test_product = {
            "name": "Jacket",
            "category": "Apparel",
            "available": True,
            "price": 89.95
        }
        response = self.client.post(
            BASE_URL,
            json=test_product,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product["name"])

    def test_update_product(self):
        """It should Update an existing Product"""
        product = Product(name="Shoes", category="Apparel", available=True, price=50.0)
        product.create()
        updated_data = {
            "name": "Shoes",
            "category": "Apparel",
            "available": False,
            "price": 40.0
        }
        response = self.client.put(
            f"{BASE_URL}/{product.id}",
            json=updated_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["available"], False)
        self.assertEqual(data["price"], 40.0)

    def test_delete_product(self):
        """It should Delete a Product"""
        product = Product(name="Socks", category="Apparel", available=True, price=5.0)
        product.create()
        response = self.client.delete(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
