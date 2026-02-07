from ..config import Session
from ..models import Product
from sqlalchemy.exc import SQLAlchemyError

class ProductRepository:
    def __init__(self):
        self.session = Session()

    def get_all_products(self):
        try:
            products = self.session.query(Product).all()
            return products
        except SQLAlchemyError as e:
            print("DB Error get_all_products:", e)
            return []
        finally:
            self.session.close()
    
    def get_product_by_id(self, product_id: int):
        try:
            return self.session.query(Product).filter(Product.id == product_id).first()
        except SQLAlchemyError as e:
            print("DB Error get_product_by_id:", e)
            return None
        finally:
            self.session.close()
    
    def create_product(self, name: str, description: str, stock: int, price: float):
        try:
            new_product = Product(name=name, description=description, stock=stock, price=price)
            self.session.add(new_product)
            self.session.commit()
            self.session.refresh(new_product)
            return new_product
        except SQLAlchemyError as e:
            self.session.rollback()
            print("DB Error create_product:", e)
            return None
        finally:
            self.session.close()
    
    def update_product(self, product_id: int, update_data: dict):
        try:
            product = self.session.query(Product).filter(Product.id == product_id).first()
            if product:
                for key, value in update_data.items():
                    if hasattr(product, key) and value is not None:
                        setattr(product, key, value)
                self.session.commit()
                self.session.refresh(product)
            return product
        except SQLAlchemyError as e:
            self.session.rollback()
            print("DB Error update_product:", e)
            return None
        finally:
            self.session.close()
    
    def delete_product(self, product_id: int):
        try:
            product = self.session.query(Product).filter(Product.id == product_id).first()
            if product:
                self.session.delete(product)
                self.session.commit()
            return product
        except SQLAlchemyError as e:
            self.session.rollback()
            print("DB Error delete_product:", e)
            return None
        finally:
            self.session.close()
