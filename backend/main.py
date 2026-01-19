from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from fastapi import HTTPException
from starlette.middleware.cors import CORSMiddleware
from models import products
from database import session, engine, Base, get_db
import database_models
from sqlalchemy.orm import Session


Products =[
    products(id=1 ,name="Laptop" , description= "A high-performance laptop", price= 999.99, quantity= 10),
    products(id=5  , name="Mobile" , description= "Android ", price= 599.00, quantity= 5)
]



def init_db():
    db = session()
    try:
        count = db.query(database_models.products).count()
        if count == 0:
            for product in Products:
                db.add(database_models.products(**product.model_dump()))
            db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):

    database_models.Base.metadata.create_all(bind=engine)
    init_db()

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    
    allow_methods=["*"]
    

)


@app.get('/')
def greet():
    return 'heyy'


@app.get('/products')
def get_all_products(db :Session = Depends(get_db)):
    
    db_products = db.query(database_models.products).all()
    return db_products

@app.get('/products/{id}')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.products).filter(database_models.products.id == id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/products")
def add_product(product: products, db: Session = Depends(get_db)):
    db.add(database_models.products(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id :int, product :products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.products).filter(database_models.products.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return product
    return "Product not found"



@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.products).filter(
        database_models.products.id == id
    ).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product does not exist"
        )

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
