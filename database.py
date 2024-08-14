from pymongo import MongoClient

client = MongoClient("mongodb+srv://harshalmahajan:Harshal%401930@mongdb.9n5po.mongodb.net/?retryWrites=true&w=majority&appName=mongdb")
db = client.JWTAUTHPROJECT
users_collection = db.jwt_users
blogging_collection = db.blogging_items
