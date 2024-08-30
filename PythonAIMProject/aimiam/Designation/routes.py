from fastapi import APIRouter,Depends
from Designation.models import DesignationModel,UpdateDesignationModel
from application.database import designation_collections
import datetime
from Designation.serializers import DecodeDesignations,DecodeDesignation
from bson import ObjectId
from fastapi import HTTPException
from utils import read_users_me



designation_root = APIRouter()
#post request
@designation_root.post("/new/designation")
def Designation(doc:DesignationModel,user: str = Depends(read_users_me)):
    #convert to dict
    doc = dict(doc)
    current_date = datetime.date.today()
    doc["date"] = str(current_date)
    
    res =  designation_collections.insert_one(doc)
    doc_id = str(res.inserted_id)

    return {
        "status" : "ok",
        "message" : "Data added successfully",
        "_id" : doc_id
    }

@designation_root.get("/all/designations")
def AllDesignation(user: str = Depends(read_users_me)):
    res = designation_collections.find()
    decoded_data = DecodeDesignations(res)

    return{

        "status" : "ok",
        "data" : decoded_data   
    }

@designation_root.get("/designation/{id}")
def getdesignation(id: int, user: str = Depends(read_users_me)):
    # Query the collection using the manually provided ID
    res = designation_collections.find_one({"id": id})
    
    if not res:
        raise HTTPException(status_code=404, detail="Designation not found")

    decoded_blog = DecodeDesignation(res)

    return {
        "status": "ok",
        "data": decoded_blog
    }

@designation_root.patch("/update/designation/{id}")

def updateDesignation(id:int, doc:UpdateDesignationModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    designation_collections.find_one_and_update(
        {"id" : id},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "Designation update successfully",
        "data" : req
    }




@designation_root.delete("/delete/{id}")
def delete_designation(id: int, user: str = Depends(read_users_me)):
    # Find and delete the document with the custom 'id' field
    result = designation_collections.find_one_and_delete({"id": id})
    
    if not result:
        raise HTTPException(status_code=404, detail="Designation not found")

    return {
        "status": "ok",
        "message": "Designation deleted successfully",
        "id": id
    }
