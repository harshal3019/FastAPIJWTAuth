from app.database import db, customer_collection, orders_collection  # Corrected variable name
from bson import ObjectId
from app.settingmail import FastMail, MessageSchema,conf
from fastapi import FastAPI, BackgroundTasks
from app.models import Customer

# Function to send email
async def send_welcome_email(email: str, name: str):
    message = MessageSchema(
        subject="Welcome to Our Service!",
        recipients=[email],  # List of recipients
        body=f"Dear {name},\n\nThank you for registering with us! We are excited to have you onboard.",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

def create_customer(customer: Customer, background_tasks: BackgroundTasks):
    # Convert Pydantic model to dictionary
    customer_data = customer.model_dump()
    
    # Insert customer into the database
    result = db.customer_collection.insert_one(customer_data)  # Use insert_one method
    
    # Schedule sending a welcome email
    background_tasks.add_task(send_welcome_email, customer.email, customer.name)
    
    # Return the inserted ID as part of the response
    return {"message": "Customer created successfully and email sent.", "customer_id": str(result.inserted_id)}

# Create a new order
def create_order(order_data):
    order = dict(order_data)
    order['customer_id'] = ObjectId(order['customer_id'])
    res = orders_collection.insert_one(order)
    return str(res.inserted_id)


def get_orders_with_customers():
    pipeline = [
        {
            "$lookup": {
                "from": "customer_collection",  # Ensure this is the correct collection name in MongoDB
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer_info"
            }
        },
        {
            "$unwind": "$customer_info"
        },
        {
            "$project": {
                "_id": {"$toString": "$_id"},  # Convert ObjectId to string
                "amount": 1,
                "customer_id": {"$toString": "$customer_id"},  # Convert ObjectId to string
                "customer_info.name": 1,
                "customer_info.email": 1
            }
        }
    ]

    results = list(orders_collection.aggregate(pipeline))
    return results
