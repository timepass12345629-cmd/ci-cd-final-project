"""
Data Models for Products Service
"""


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class Product:
    """
    Class that represents a Product
    """
    id_counter = 0
    data = {}

    def __init__(self, id=0, name="", category="", available=True, price=0.0):
        self.id = id
        self.name = name
        self.category = category
        self.available = available
        self.price = float(price)

    def create(self):
        """Creates a Product and assigns an ID"""
        Product.id_counter += 1
        self.id = Product.id_counter
        Product.data[self.id] = self
        return self

    def update(self):
        """Updates a Product in the database"""
        if not self.id or self.id not in Product.data:
            raise DataValidationError(f"Product with id {self.id} not found")
        Product.data[self.id] = self
        return self

    def delete(self):
        """Deletes a Product from the database"""
        if self.id in Product.data:
            del Product.data[self.id]

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "available": self.available,
            "price": self.price,
        }

    def deserialize(self, data):
        """Deserializes a Product from a dictionary"""
        try:
            self.name = data["name"]
            self.category = data["category"]
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError("Invalid type for boolean [available]: " + str(type(data["available"])))
            self.price = float(data["price"])
        except KeyError as error:
            raise DataValidationError("Invalid Product: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError("Invalid Product: body of request contained bad or no data: " + str(error))
        return self

    @classmethod
    def all(cls):
        """Returns all Products"""
        return list(cls.data.values())

    @classmethod
    def find(cls, product_id):
        """Finds a Product by ID"""
        return cls.data.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        """Finds Products by Name"""
        return [prod for prod in cls.data.values() if prod.name.lower() == name.lower()]

    @classmethod
    def remove_all(cls):
        """Removes all Products from the collection"""
        cls.data.clear()
        cls.id_counter = 0
