from pydantic import BaseModel

class BlogModel(BaseModel):
    title : str
    sub_title : str
    content : str
    author : str


class updateBlogModel(BaseModel):
    title : str = None
    sub_title : str = None
    content : str = None
    author : str = None
  