from flask import Blueprint, request, jsonify, g
from ..services import ProductService
from ..middlewares.token_required import token_required

product_bp = Blueprint("product", __name__)
service = ProductService()

@product_bp.route("/product")
@token_required
def get_products():
    user = g.user  
    products = service.list_products()
    list_products = [p.to_dict() for p in products]

    return jsonify({
        "user": user.username,
        "products": list_products
    })


@product_bp.route("/product/<int:product_id>")
@token_required
def get_product(product_id):
    user = g.user
    product = service.get_product(product_id=product_id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({
        "user": user.username,
        "product": product.to_dict()
    })


@product_bp.route("/product", methods=["POST"])
@token_required
def create_product():
    user = g.user
    data = request.json

    name = data.get("name")
    description = data.get("description")
    stock = data.get("stock")
    price = data.get("price")

    if not all([name, description, stock, price]):
        return jsonify({"error": "Missing fields"}), 400

    product = service.append_product(name=name, description=description, stock=stock, price=price)

    return jsonify({
        "message": f"Product {product.name} created by {user.username}"
    }), 201


@product_bp.route("/product/<int:product_id>", methods=["PUT"])
@token_required
def update_product(product_id):
    user = g.user
    data = request.json

    product = service.edit_product(product_id, data)
    if product:
        return jsonify({
            "message": f"Product {product.name} updated by {user.username}"
        })
    return jsonify({"error": "Product not found"}), 404


@product_bp.route("/product/<int:product_id>", methods=["DELETE"])
@token_required
def delete_product(product_id):
    user = g.user
    product = service.remove_product(product_id)
    if product:
        return jsonify({
            "message": f"Product {product.name} deleted by {user.username}"
        })
    return jsonify({"error": "Product not found"}), 404
