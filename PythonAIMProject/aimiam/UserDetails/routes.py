from fastapi import BackgroundTasks, Depends, HTTPException, status,APIRouter
# from fastapi_mail import MessageSchema, FastMail,conf
from application.Setting import MessageSchema,conf,FastMail
from pydantic import EmailStr
from datetime import datetime
from bson import ObjectId
from application.database import userdetails_collections,user_collections
from UserDetails.models import UserDetailsModel
from utils import read_users_me
from application.auth import get_password_hash

userdetails_root = APIRouter()

# Function to send registration email
async def send_registration_email(email: EmailStr, username: str, password: str):
    message = MessageSchema(
        subject="Welcome to Our Service",
        recipients=[email],
        body=f"""
        Hi {username},
        Welcome to our service! Here are your login details:

        Username: {username}
        Password: {password}

        Please keep this information safe.
        """,
        subtype="plain"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

# Function to check if user exists in both collections
def check_user_exists(email: str, username: str):
    user_in_user_collection = user_collections.find_one({"$or": [{"email": email}, {"username": username}]})
    user_in_userdetails_collection = userdetails_collections.find_one({"$or": [{"email": email}, {"username": username}]})
    return user_in_user_collection, user_in_userdetails_collection

# Endpoint to add user details and handle dual collection insertion
@userdetails_root.post('/add/userdetails')
def UserDetails(doc: UserDetailsModel, background_tasks: BackgroundTasks):
    
    # Check if the user already exists in both collections
    user_in_user_collection, user_in_userdetails_collection = check_user_exists(doc.email, doc.username)

    # Store the original password before hashing
    original_password = doc.password

    # Hash the password for storage
    hashed_password = get_password_hash(doc.password)
    
    # Insert into `user_collection` if not present
    if not user_in_user_collection:
        user_data = {
            "username": doc.username,
            "email": doc.email,
            "password": hashed_password
        }
        user_collections.insert_one(user_data)

    # Insert into `userdetails_collection` if not present
    if not user_in_userdetails_collection:
        user_details_data = dict(doc)
        user_details_data["password"] = hashed_password
        userdetails_collections.insert_one(user_details_data)

    # Send registration email only if the user was inserted into `user_collection`
    if not user_in_user_collection:
        background_tasks.add_task(send_registration_email, doc.email, doc.username, original_password)

    return {
        "status": "ok",
        "message": "UserDetails processed successfully"
    }


def get_permissions_with_joins():
    pipeline = [
        # Lookup and join customer data
        {
            "$lookup": {
                "from": "customer_collection",  # Name of the customer collection
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer_info"
            }
        },
        {
            "$unwind": "$customer_info"
        },

        # # Lookup and join role data
        # {
        #     "$lookup": {
        #         "from": "role_collection",  # Name of the role collection
        #         "localField": "role_id",
        #         "foreignField": "_id",
        #         "as": "role_info"
        #     }
        # },
        # {
        #     "$unwind": "$role_info"
        # },

        # # Lookup and join department data
        # {
        #     "$lookup": {
        #         "from": "department_collection",  # Name of the department collection
        #         "localField": "dept_id",
        #         "foreignField": "_id",
        #         "as": "department_info"
        #     }
        # },
        # {
        #     "$unwind": "$department_info"
        # },

        # # Lookup and join designation data
        # {
        #     "$lookup": {
        #         "from": "designation_collection",  # Name of the designation collection
        #         "localField": "designation_id",
        #         "foreignField": "_id",
        #         "as": "designation_info"
        #     }
        # },
        # {
        #     "$unwind": "$designation_info"
        # },

        # Project the required fields
        {
            "$project": {
                "_id": {"$toString": "$_id"},  # Convert ObjectId to string
                "amount": 1,
                "customer_id": {"$toString": "$customer_id"},  # Convert ObjectId to string
                "customer_info.name": 1,
                "customer_info.email": 1,
                "role_info.role_name": 1,  # Adjust field names according to your schema
                "department_info.department_name": 1,  # Adjust field names according to your schema
                "designation_info.designation_name": 1  # Adjust field names according to your schema
            }
        }
    ]

    results = list(permission_collections.aggregate(pipeline))
    return results