from pymongo import MongoClient

client = MongoClient("mongodb+srv://harshalmahajan:Harshal%401930@mongdb.9n5po.mongodb.net/?retryWrites=true&w=majority&appName=mongdb")
db = client["aimiam_db"]
user_collections = db["user_collections"]
designation_collections = db["desgination_collection"]
department_collections = db["department_collection"]
role_collections = db["role_collections"]
permission_collections = db['permission_collection']
userdetails_collections = db['userdetails_collection']