from flask import Blueprint, request, jsonify
from ..services import OrderService

order_bp = Blueprint("order",__name__)
service = OrderService()

@order_bp.route("/order", methods=["GET"])
def get_orders():
    orders = service.list_orders()
    return jsonify([{
        "id": o.id,
        "customer_name": o.customer_name,
        "created_at": o.created_at.isoformat(),
        "total_price": float(o.total_price),
        "items": [{
            "product_id": i.product_id,
            "quantity": i.quantity,
            "price": float(i.price)
        } for i in o.items]
    } for o in orders])


@order_bp.route("/order/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = service.get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({
        "id": order.id,
        "customer_name": order.customer_name,
        "created_at": order.created_at.isoformat(),
        "total_price": float(order.total_price),
        "items": [{
            "product_id": i.product_id,
            "quantity": i.quantity,
            "price": float(i.price)
        } for i in order.items]
    })

@order_bp.route("/order", methods=["POST"])
def create_order():
    data = request.json
    customer_name = data.get("customer_name")
    items = data.get("items", [])

    if not customer_name or not items:
        return jsonify({"error": "Customer name and items are required"}), 400

    order = service.create_order(customer_name, items)
    return jsonify({"id": order.id, "message": "Order created"}), 201

@order_bp.route("/order/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.json
    order = service.update_order(order_id, data)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "total_price": float(order.total_price),
        "items": [{
            "product_id": i.product_id,
            "quantity": i.quantity,
            "price": float(i.price)
        } for i in order.items],
        "message": "Order updated"
    })

@order_bp.route("/order/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = service.delete_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"message": "Order deleted"})