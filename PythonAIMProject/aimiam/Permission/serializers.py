def DecodePermission(doc) -> dict:
    return {
        "_id" : str(doc["_id"]) ,
        "permission_name" : doc["permission_name"] ,
        "permission_id" : doc["permission_id"] ,
        "category" : doc["category"],
        "Type" : doc["Type"],
        "Description" : doc["Description"],
        "status" : doc["status"]
        
    }

# all blogs 
def DecodePermissions(docs) -> list:
    return [DecodePermission(doc) for doc in docs]