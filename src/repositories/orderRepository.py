from ..config import Session
from ..models import Order,OrderItem,Product
from sqlalchemy.orm import joinedload

class OrderRepository:
    def __init__(self):
        self.session = Session()

    def get_all_orders(self):
        orders = self.session.query(Order).options(joinedload(Order.items)).all()
        self.session.close()
        return orders
    
    def get_order_by_id(self, order_id: int):
        order = (
            self.session.query(Order)
            .options(joinedload(Order.items))  
            .filter(Order.id == order_id)
            .first()
        )
        self.session.close()
        return order

    def create_order(self, customer_name: str, items: list):
        new_order = Order(customer_name=customer_name)

        total_price = 0
        for item in items:
            product = self.session.query(Product).filter(Product.id == item["product_id"]).first()
            if not product:
                continue
            price = product.price * item["quantity"]
            total_price += price
            order_item = OrderItem(
                product_id=product.id,
                quantity=item["quantity"],
                price=price
            )
            new_order.items.append(order_item)

        new_order.total_price = total_price
        self.session.add(new_order)
        self.session.commit()
        self.session.refresh(new_order)
        self.session.close()
        return new_order
    


    def get_order_by_id(self, order_id: int):
        order = (
            self.session.query(Order)
            .options(joinedload(Order.items))  
            .filter(Order.id == order_id)
            .first()
        )
        self.session.close()
        return order
    
    def update_order(self, order_id: int, update_data: dict):
        order = (
            self.session.query(Order)
            .options(joinedload(Order.items))  
            .filter(Order.id == order_id)
            .first()
        )
        if not order:
            self.session.close()
            return None

     
        if "customer_name" in update_data:
            order.customer_name = update_data["customer_name"]
        if "status" in update_data:
            order.status = update_data["status"]

    
        if "items" in update_data:
            new_items = update_data["items"]
           
            existing_items_dict = {item.product_id: item for item in order.items}

            updated_items = []

            for item_data in new_items:
                product_id = item_data["product_id"]
                quantity = item_data.get("quantity", 1)
                
                product = self.session.query(Product).filter(Product.id == product_id).first()
                if not product:
                    continue
                price = product.price * quantity

                if product_id in existing_items_dict:
                    order_item = existing_items_dict[product_id]
                    order_item.quantity = quantity
                    order_item.price = price
                else:
                  
                    order_item = OrderItem(
                        product_id=product_id,
                        quantity=quantity,
                        price=price
                    )
                    order.items.append(order_item)

                updated_items.append(order_item)

          
            for item in order.items[:]:
                if item.product_id not in [i.product_id for i in updated_items]:
                    self.session.delete(item)

    
        order.total_price = sum([item.price for item in order.items])

        self.session.commit()
        self.session.refresh(order)
        self.session.close()
        return order
    
    def delete_order(self, order_id: int):
        order = self.session.query(Order).filter(Order.id == order_id).first()
        if order:
            self.session.delete(order)
            self.session.commit()
        self.session.close()
        return order

