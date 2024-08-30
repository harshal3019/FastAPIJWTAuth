def DecodeRole(doc) -> dict:
    return {
        "_id" : str(doc["_id"]) ,
        "role_name" : doc["role_name"] ,
        "role_id" : doc["role_id"] ,
        "description" : doc['description'],
        "status" : doc["status"]
        
    }

# all blogs 
def DecodeRoles(docs) -> list:
    return [DecodeRole(doc) for doc in docs]