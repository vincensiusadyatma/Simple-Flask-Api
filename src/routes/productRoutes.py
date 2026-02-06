from flask import Blueprint, request, jsonify
from ..services import ProductService

product_bp = Blueprint("product",__name__)
service = ProductService()

@product_bp .route("/product")
def get_products():
    products = service.list_products()
    list_products = []

    for product in products:
        product_dict = product.to_dict()
        list_products.append(product_dict)

    return jsonify({
        "products" : list_products
    })

@product_bp.route("/product/<int:product_id>")
def get_product(product_id):
    product = service.get_product(product_id=product_id)
    return jsonify({
        "product" : {
            "name" : product.name,
            "description" : product.description,
            "stock" : product.stock,
            "price" : product.price
        }
    })

@product_bp.route("/product", methods=["POST"])
def create_product():
    data = request.json
    name = data["name"]
    description = data["description"]
    stock = data["stock"]
    price = data["price"]


    product = service.append_product(name=name,description=description,stock=stock,price=price)
    return jsonify({
        "message" : "bagus"
    }), 201

@product_bp.route("/product/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    product = service.edit_product(product_id, data)
    if product:
        return jsonify({
            "message" : "update succes"
        })
    return jsonify({"error": "Product not found"}), 404

@product_bp.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = service.remove_product(product_id)
    if product:
        return jsonify({"data": f"Product {product_id} deleted", "error": None})
    return jsonify({"data": None, "error": "Product not found"}), 404