from flask import Blueprint, request, jsonify, g
from ..services import OrderService
from ..middlewares.token_required import token_required

order_bp = Blueprint("order", __name__)
service = OrderService()

@order_bp.route("/order", methods=["GET"])
@token_required
def get_orders():
    try:
        user = g.user
        orders = service.list_orders()
        return jsonify({
            "status": "success",
            "user": user.username,
            "orders": [{
                "id": o.id,
                "customer_name": o.customer_name,
                "created_at": o.created_at.isoformat(),
                "total_price": float(o.total_price),
                "items": [{
                    "product_id": i.product_id,
                    "quantity": i.quantity,
                    "price": float(i.price)
                } for i in o.items]
            } for o in orders]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@order_bp.route("/order/<int:order_id>", methods=["GET"])
@token_required
def get_order(order_id):
    try:
        user = g.user
        order = service.get_order(order_id)
        if not order:
            return jsonify({"status": "error", "error": "Order not found"}), 404
        return jsonify({
            "status": "success",
            "user": user.username,
            "order": {
                "id": order.id,
                "customer_name": order.customer_name,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "total_price": float(order.total_price),
                "items": [{
                    "product_id": i.product_id,
                    "quantity": i.quantity,
                    "price": float(i.price)
                } for i in order.items]
            }
        }), 200
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@order_bp.route("/order", methods=["POST"])
@token_required
def create_order():
    try:
        user = g.user
        data = request.json
        customer_name = data.get("customer_name")
        items = data.get("items", [])

        order = service.create_order(customer_name, items)
        if not order:
            return jsonify({"status": "error", "error": "Failed to create order"}), 400

        return jsonify({
            "status": "success",
            "message": f"Order {order.id} created by {user.username}",
            "order_id": order.id
        }), 201
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@order_bp.route("/order/<int:order_id>", methods=["PUT"])
@token_required
def update_order(order_id):
    try:
        user = g.user
        data = request.json
        order = service.update_order(order_id, data)
        if not order:
            return jsonify({"status": "error", "error": "Order not found"}), 404
        return jsonify({
            "status": "success",
            "message": f"Order {order.id} updated by {user.username}",
            "order_id": order.id
        }), 200
    except ValueError as ve:
        return jsonify({"status": "error", "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@order_bp.route("/order/<int:order_id>", methods=["DELETE"])
@token_required
def delete_order(order_id):
    try:
        user = g.user
        order = service.delete_order(order_id)
        if not order:
            return jsonify({"status": "error", "error": "Order not found"}), 404
        return jsonify({
            "status": "success",
            "message": f"Order {order.id} deleted by {user.username}"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
