from fastapi import FastAPI,APIRouter,Depends,HTTPException
from Permission.models import PermissionModel,updatePermissionModel
from utils import read_users_me
import datetime
from application.database import permission_collections
from Permission.serializers import DecodePermission,DecodePermissions



permission_root = APIRouter()


@permission_root.post('/add/permission')
def Permission(doc:PermissionModel,user: str = Depends(read_users_me)):
    doc = dict(doc)
    current_date = datetime.date.today()
    doc["date"] = str(current_date)
    
    res =  permission_collections.insert_one(doc)
    doc_id = str(res.inserted_id)

    return {
        "status" : "ok",
        "message" : "Permission  added successfully",
        "_id" : doc_id
    }

@permission_root.get("/all/permission")
def AllPermission(user: str = Depends(read_users_me)):
    res = permission_collections.find({"status": 1})
    decoded_data = DecodePermissions(res)

    return{

        "status" : "ok",
        "data" : decoded_data   
    }


@permission_root.get("/permission/{id}")
def getpermission(id: int, user: str = Depends(read_users_me)):
    # Query the collection using the manually provided ID
    res = permission_collections.find_one({"permission_id": id,"status": 1})
    
    if not res:
        raise HTTPException(status_code=404, detail="permission not found")

    decoded_permission = DecodePermission(res)

    return {
        "status": "ok",
        "data": decoded_permission
    }

@permission_root.patch("/update/permission/{id}")

def updatePermission(id:int, doc:updatePermissionModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    permission_collections.find_one_and_update(
        {"permission_id" : id},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "Permission update successfully",
        "data" : req
    }


@permission_root.patch("/delete/permission/{id}")

def updateDepartment(id:int, doc:updatePermissionModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    permission_collections.find_one_and_update(
        {"permission_id" : id},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "Permission Deleted successfully",
        "data" : req
    }