from ..repositories import ProductRepository

class ProductService:
    def __init__(self):
        self.repo = ProductRepository()
    
    def list_products(self):
        return self.repo.get_all_products()
    
    def get_product(self, product_id: int):
        if not product_id:
            raise ValueError("product_id is required")
        return self.repo.get_product_by_id(product_id)
    
    def append_product(self, name: str, description: str, stock: int, price: float):
        if not all([name, description, stock, price]):
            raise ValueError("All fields (name, description, stock, price) are required")
        return self.repo.create_product(name, description, stock, price)
    
    def edit_product(self, product_id: int, data: dict):
        if not data:
            raise ValueError("No data provided for update")
        return self.repo.update_product(product_id, data)
    
    def remove_product(self, product_id: int):
        return self.repo.delete_product(product_id)
