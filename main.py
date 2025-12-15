from fastapi import FastAPI, Depends
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

products = [
    Product(id=1, name="laptop", price=999.99),
    Product(id=2, name="smart phone", price=99.99),
    Product(id=3, name="smart watch", price=9.99),
    Product(id=4, name="monitor", price=12.99),
]


# when db is empty populate with initial data
def init_db():
    db = session()
    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()


init_db()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# get all products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


# get single product using id
@app.get("/products/{id}")
def get_single_product(id: int, db: Session = Depends(get_db)):
    product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )
    if product:
        return product

    return "product not found"


# add a product
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "product added succcessfully"


# update a product
@app.put("/products")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db.commit()
        return "product updated successfully"
    else:
        return "product not found"


# delete a product
@app.delete("/products")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )
    if db_product:
        db.delete(db_product)
        db.commit()
        return f"{db_product.name} delted successfully"
    else:
        return "Product not found"


"""
# get all products
@app.get("/products")
def get_products():
    return products


# get single product using id
@app.get("/products/{id}")
def get_single_product(id: int):
    for product in products:
        if product.id == id:
            return product

    return "product not found"


# add a product
@app.post("/products")
def add_product(product: Product):
    products.append(product)


# update a product
@app.put("/products")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        print(id)
        print(product)
        if products[i].id == id:
            products[i] = product
            return "Product updated succcessfully"

    return


# delete a product
@app.delete("/products")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deletd successfully"

    return "Product not found"

"""
