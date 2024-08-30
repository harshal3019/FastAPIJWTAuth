from pymongo import MongoClient
import pprint


# client = MongoClient("mongodb+srv://harshalmahajan:Harshal%401930@mongdb.9n5po.mongodb.net/?retryWrites=true&w=majority&appName=mongdb")
# db = client.LookupDatabase
# cust_collection = db.customer_collection
# orders_collections = db.order_collections

# Check type in orders_collection
# orders_collection = db.order_collections
# sample_order = orders_collection.find_one({}, {"customer_id": 1})
# print("Type of customer_id in orders_collection:", type(sample_order.get("customer_id")))

# Check type in cust_collection
# cust_collection = db.customer_collection
# sample_customer = cust_collection.find_one({}, {"_id": 1})
# print("Type of _id in cust_collection:", type(sample_customer.get("_id")))

# Print sample document from orders_collection
# sample_order = db.order_collections.find_one()
# print(sample_order)

# # Print sample document from cust_collection
# sample_customer = db.customer_collection.find_one()
# print(sample_customer)

# Fetch data using the pipeline
# Define the aggregation pipeline
# MongoDB connection
client = MongoClient("mongodb+srv://harshalmahajan:Harshal%401930@mongdb.9n5po.mongodb.net/?retryWrites=true&w=majority&appName=mongdb")
db = client["LookupDatabase"]
customer_collection = db["customer_collection"]
orders_collection = db["order_collections"]

print("Connecting to MongoDB...")  # Check connection

# # Define the aggregation pipeline
# pipeline = [
#     {
#         "$lookup": {
#             "from": "customer_collection",          # The collection to join with
#             "localField": "customer_id",  # Field in the orders collection
#             "foreignField": "_id",        # Field in the customers collection
#             "as": "customer_info"         # The name of the new array field with the joined data
#         }
#     },
#       {
#         "$unwind": "$customer_info"  # Flatten the customer_info array if it contains only one element
#     },
#     {
#         "$project": {
#             "_id": 1,               
#             "amount": 1,             
#             "customer_id": 1,        
#             "customer_info.name": 1,
#             "customer_info.email": 1 
#         }
#     }
    
# ]

# # Perform the aggregation
# results = list(orders_collection.aggregate(pipeline))
# return results


