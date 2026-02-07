from flask import Blueprint, request, jsonify, g
from ..services import OrderService
from ..middlewares.token_required import token_required

order_bp = Blueprint("order",__name__)
service = OrderService()

@order_bp.route("/order", methods=["GET"])
@token_required
def get_orders():
    orders = service.list_orders()
    user = g.user  
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
@token_required
def get_order(order_id):
    order = service.get_order(order_id)
    user = g.user  
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
@token_required
def create_order():
    data = request.json
    user = g.user  
    customer_name = data.get("customer_name")
    items = data.get("items", [])

    if not customer_name or not items:
        return jsonify({"error": "Customer name and items are required"}), 400

    order = service.create_order(customer_name, items)
    return jsonify({"id": order.id, "message": "Order created"}), 201

@order_bp.route("/order/<int:order_id>", methods=["PUT"])
@token_required
def update_order(order_id):
    user = g.user  
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
@token_required
def delete_order(order_id):
    user = g.user  
    order = service.delete_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"message": "Order deleted"})