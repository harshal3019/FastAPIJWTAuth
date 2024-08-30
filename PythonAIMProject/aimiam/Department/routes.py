from fastapi import FastAPI,APIRouter,Depends,HTTPException
from Department.models import DepartmentModel,UpdateDepartmentModel
import datetime
from utils import read_users_me
from application.database import department_collections
from Department.serializers import DecodeDepartments,DecodeDepartment



department_root  = APIRouter()

#post request
@department_root.post("/new/department")
def NewDepartment(doc:DepartmentModel,user: str = Depends(read_users_me)):
    #convert to dict
    doc = dict(doc)
    current_date = datetime.date.today()
    doc["date"] = str(current_date)
    
    res =  department_collections.insert_one(doc)
    doc_id = str(res.inserted_id)

    return {
        "status" : "ok",
        "message" : "Department added successfully",
        "_id" : doc_id
          
    }

@department_root.get("/all/department")
def AllDepartment(user: str = Depends(read_users_me)):
    res = department_collections.find({"status": 1})
    decoded_data = DecodeDepartments(res)

    return{

        "status" : "ok",
        "data" : decoded_data   
    }

@department_root.get("/department/{id}")
def getdesignation(id: int, user: str = Depends(read_users_me)):
    # Query the collection using the manually provided ID
    res = department_collections.find_one({"dept_id": id,"status": 1})
    
    if not res:
        raise HTTPException(status_code=404, detail="Designation not found")

    decoded_department = DecodeDepartment(res)

    return {
        "status": "ok",
        "data": decoded_department
    }


@department_root.patch("/update/department/{id}")

def updateDepartment(id:int, doc:UpdateDepartmentModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    department_collections.find_one_and_update(
        {"dept_id" : id},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "Department update successfully",
        "data" : req
    }


@department_root.patch("/delete/department/{id}")

def updateDepartment(id:int, doc:UpdateDepartmentModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    department_collections.find_one_and_update(
        {"dept_id" : id},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "Department Deleted successfully",
        "data" : req
    }