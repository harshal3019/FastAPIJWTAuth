# one doc 
def DecodeDesignation(doc) -> dict:
    return {
        "_id" : str(doc["_id"]) ,
        "designation_name" : doc["designation_name"] ,
        "id" : doc["id"] ,
        
    }

# all blogs 
def DecodeDesignations(docs) -> list:
    return [DecodeDesignation(doc) for doc in docs]