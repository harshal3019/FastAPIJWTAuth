from fastapi import APIRouter,Depends
from model.Blog import BlogModel,updateBlogModel
from database import blogging_collection
import datetime
from serializers.blog import DecodeBlogs,DecodeBlog
from bson import ObjectId
from fastapi import HTTPException
from utils import read_users_me

blog_root = APIRouter()

#post request
@blog_root.post("/new/blog")
def NewBlog(doc:BlogModel,user: str = Depends(read_users_me)):
    #convert to dict
    doc = dict(doc)
    current_date = datetime.date.today()
    doc["date"] = str(current_date)
    
    res =  blogging_collection.insert_one(doc)
    doc_id = str(res.inserted_id)

    return {
        "status" : "ok",
        "message" : "Data added successfully",
        "_id" : doc_id
    }

@blog_root.get("/all/blogs")
def AllBlog(user: str = Depends(read_users_me)):
    res = blogging_collection.find()
    decoded_data = DecodeBlogs(res)

    return{

        "status" : "ok",
        "data" : decoded_data   
    }
@blog_root.get("/blogs/{_id}")
def getBlog(_id:str,user: str = Depends(read_users_me)):

    res = blogging_collection.find_one({"_id": ObjectId(_id)})
    decoded_blog = DecodeBlog(res)

    return{

         "status" : "ok",
         "data" : decoded_blog

    }

@blog_root.patch("/update/blogs/{_id}")

def updateBlog(_id:str, doc:updateBlogModel,user: str = Depends(read_users_me)):

    req = dict(doc.model_dump(exclude_unset=True))

    blogging_collection.find_one_and_update(
        {"_id" : ObjectId(_id)},
        {"$set" : req}
    )

    return {

        "status" : "okay",
        "message" : "blog update successfully"
    }
   #delete
@blog_root.delete("/delete/{_id}")
def deleteBlog(_id:str,user: str = Depends(read_users_me)) :
    blogging_collection.find_one_and_delete(
        {"_id" : ObjectId(_id)}
    )

    return {
        "status" : "okay",
        "message" : "blog deleted successfully"
    }