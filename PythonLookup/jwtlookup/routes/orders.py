from fastapi import APIRouter
from app.crud import create_customer,create_order,get_orders_with_customers
from app.models import Customer, Order
from fastapi import FastAPI, BackgroundTasks


router = APIRouter()

@router.post("/customers")
async def add_customer(customer: Customer, background_tasks: BackgroundTasks):
    customer_id = create_customer(customer, background_tasks)
    return {"status": "success", "customer_id": customer_id}

@router.post("/orders")
async def add_order(order: Order):
    order_id = create_order(order)
    return {"status": "success", "order_id": order_id}

@router.get("/orders")
async def list_orders():
    orders = get_orders_with_customers()
    return {"status": "success", "data": orders}