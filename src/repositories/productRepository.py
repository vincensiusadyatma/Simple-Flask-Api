from ..config import Session
from ..models import Product

class ProductRepository:
    def __init__(self):
        self.session = Session()

    def get_all_products(self):
        products = self.session.query(Product).all()
        self.session.close()
        return products
    
    def get_product_by_id(self,product_id: int):
        product = self.session.query(Product).filter(Product.id == product_id).first()
        self.session.close()
        return product
    
    def create_product(self,name:str,description:str,stock:int, price:float):
        new_product = Product(name=name,description=description,stock=stock,price=price)
        self.session.add(new_product)
        self.session.commit()
        self.session.refresh(new_product)
        self.session.close()
        return new_product
    
    def update_product(self,product_id: int, update_data: dict):
        product = self.session.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in update_data.items():
                setattr(product, key, value)
            self.session.commit()
            self.session.refresh(product)
        self.session.close()
        return product
    
    def delete_product(self,product_id: int):
        product = self.session.query(Product).filter(Product.id == product_id).first()
        if product:
            self.session.delete(product)
            self.session.commit()
        self.session.close()
        return product