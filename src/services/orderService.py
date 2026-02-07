from ..repositories import OrderRepository

class OrderService:
    def __init__(self):
        self.repo = OrderRepository()

    def list_orders(self):
        return self.repo.get_all_orders()

    def get_order(self, order_id: int):
        if not order_id:
            raise ValueError("order_id is required")
        return self.repo.get_order_by_id(order_id)

    def create_order(self, customer_name: str, items: list):
        return self.repo.create_order(customer_name, items)

    def update_order(self, order_id: int, update_data: dict):
        if not update_data:
            raise ValueError("No data provided for update")
        return self.repo.update_order(order_id, update_data)

    def delete_order(self, order_id: int):
        return self.repo.delete_order(order_id)
