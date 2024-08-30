from fastapi import FastAPI,APIRouter,Depends,HTTPException
from Roles.models import RolesModel,UpdateRolesModel
from utils import read_users_me
from application.database import role_collections
import datetime
from Roles.serializers import DecodeRoles,DecodeRole



roles_root = APIRouter()

@roles_root.post("/new/roles")
def NewRoles(doc:RolesModel,user: str = Depends(read_users_me)):
    #convert to dict
    doc = dict(doc)
    current_date = datetime.date.today()
    doc["date"] = str(current_date)
    
    res =  role_collections.insert_one(doc)
    doc_id = str(res.inserted_id)

    return {
        "status" : "ok",
        "message" : "Roles added successfully",
        "_id" : doc_id
          
    }

@roles_root.get("/all/roles")
def AllRoles(user: str = Depends(read_users_me)):
    res = role_collections.find({"status": 1})
    decoded_data = DecodeRoles(res)

    return{

        "status" : "ok",
        "data" : decoded_data   
    }

@roles_root.get("/roles/{id}")
def getroles(id: int, user: str = Depends(read_users_me)):
    # Query the collection using the manually provided ID
    res = role_collections.find_one({"role_id": id,"status": 1})
    
    if not res:
        raise HTTPException(status_code=404, detail="Designation not found")

    decoded_blog = DecodeRole(res)

    return {
        "status": "ok",
        "data": decoded_blog
    }

@roles_root.patch("/update/roles/{id}")

def updateRoles(id:int, doc:UpdateRolesModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    role_collections.find_one_and_update(
        {"role_id" : id},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "Designation update successfully",
        "data" : req
    }

@roles_root.patch("/delete/roles/{id}")

def deleteRoles(id:int, doc:UpdateRolesModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    role_collections.find_one_and_update(
        {"role_id" : id},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "Department Deleted successfully",
        "data" : req
    }