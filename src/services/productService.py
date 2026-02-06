from ..repositories import ProductRepository

class ProductService:
    def __init__(self):
        self.repo = ProductRepository()
    
    def list_products(self):
        return self.repo.get_all_products()
    
    def get_product(self,product_id: int):
        return self.repo.get_product_by_id(product_id)
    
    def append_product(self,name:str,description:str,stock:int, price:float):
        return self.repo.create_product(name,description,stock,price)
    
    def edit_product(self,product_id: int, data: dict):
        return self.repo.update_product(product_id, data)
    
    def remove_product(self,product_id: int):
        return self.repo.delete_product(product_id)