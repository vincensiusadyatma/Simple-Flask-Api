from flask import Blueprint, request, jsonify, g
from ..services import ProductService
from ..middlewares.token_required import token_required

product_bp = Blueprint("product", __name__)
service = ProductService()

@product_bp.route("/product")
@token_required
def get_products():
    try:
        user = g.user
        products = service.list_products()
        list_products = [p.to_dict() for p in products]
        return jsonify({
            "status": "success",
            "user": user.username,
            "products": list_products
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@product_bp.route("/product/<int:product_id>")
@token_required
def get_product(product_id):
    try:
        user = g.user
        product = service.get_product(product_id)
        if not product:
            return jsonify({"status": "error", "error": "Product not found"}), 404
        return jsonify({
            "status": "success",
            "user": user.username,
            "product": product.to_dict()
        }), 200
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@product_bp.route("/product", methods=["POST"])
@token_required
def create_product():
    try:
        user = g.user
        data = request.json
        name = data.get("name")
        description = data.get("description")
        stock = data.get("stock")
        price = data.get("price")
        product = service.append_product(name, description, stock, price)
        if not product:
            return jsonify({"status": "error", "error": "Failed to create product"}), 500
        return jsonify({
            "status": "success",
            "message": f"Product {product.name} created by {user.username}"
        }), 201
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@product_bp.route("/product/<int:product_id>", methods=["PUT"])
@token_required
def update_product(product_id):
    try:
        user = g.user
        data = request.json
        product = service.edit_product(product_id, data)
        if not product:
            return jsonify({"status": "error", "error": "Product not found"}), 404
        return jsonify({
            "status": "success",
            "message": f"Product {product.name} updated by {user.username}"
        }), 200
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@product_bp.route("/product/<int:product_id>", methods=["DELETE"])
@token_required
def delete_product(product_id):
    try:
        user = g.user
        product = service.remove_product(product_id)
        if not product:
            return jsonify({"status": "error", "error": "Product not found"}), 404
        return jsonify({
            "status": "success",
            "message": f"Product {product.name} deleted by {user.username}"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
