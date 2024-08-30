def DecodeDepartment(doc) -> dict:
    return {
        "_id" : str(doc["_id"]) ,
        "department_name" : doc["department_name"] ,
        "dept_id" : doc["dept_id"] ,
        "status" : doc["status"]
        
    }

# all blogs 
def DecodeDepartments(docs) -> list:
    return [DecodeDepartment(doc) for doc in docs]