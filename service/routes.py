"""
Product Service RESTful API Routes
"""
from flask import jsonify, request, abort
from service import app
from service.models import Product, DataValidationError
from service.common import status


@app.route("/")
def index():
    """Root URL response"""
    return jsonify({
        "name": "Product Demo REST API Service",
        "version": "1.0.0",
        "status": "SERVICERUNNING",
        "port": 8000,
        "paths": {
            "health": "/health",
            "products": "/products"
        }
    }), status.HTTP_200_OK


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify(status="OK"), status.HTTP_200_OK


@app.route("/products", methods=["GET"])
def list_products():
    """Returns all Products or filters by name"""
    name = request.args.get("name")
    if name:
        products = Product.find_by_name(name)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Retrieve a single Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products", methods=["POST"])
def create_product():
    """Creates a Product"""
    check_content_type("application/json")
    product = Product()
    try:
        product.deserialize(request.get_json())
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))

    product.create()
    location_url = f"/products/{product.id}"
    return jsonify(product.serialize()), status.HTTP_201_CREATED, {"Location": location_url}


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Updates a Product"""
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    try:
        product.deserialize(request.get_json())
        product.id = product_id
        product.update()
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))

    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Deletes a Product"""
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if not content_type or content_type != media_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {media_type}")


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles bad requests with 400_BAD_REQUEST"""
    return jsonify({"error": "Bad Request", "message": str(error)}), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles resources not found with 404_NOT_FOUND"""
    return jsonify({"error": "Not Found", "message": str(error)}), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """Handles unsupported media type with 415_UNSUPPORTED_MEDIA_TYPE"""
    return jsonify({"error": "Unsupported Media Type", "message": str(error)}), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

