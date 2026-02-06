from ..models import Product
from ..config import Session

db = Session()

data  = [
    Product(
            name="Laptop",
            description="Laptop gaming",
            price=15000000,
            stock=10
    ),
    Product(
            name="Mouse",
            description="Mouse wireless",
            price=250000,
            stock=50
    )
]

def productSeed():
    db.add_all(data)
    db.commit()
    db.close()


