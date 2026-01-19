from pydantic import BaseModel
class products(BaseModel):
    id : int
    name : str
    description : str
    price :float
    quantity: int
