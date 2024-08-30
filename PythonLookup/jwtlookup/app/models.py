from pydantic import BaseModel, EmailStr
from bson import ObjectId

class Customer(BaseModel):
    name: str
    email: EmailStr
    customer_id : str
    xyz:str
    
class Order(BaseModel):
    product: str
    amount: float
    customer_id: str  # Store as string, but convert to ObjectId in CRUD
    user_id: str
