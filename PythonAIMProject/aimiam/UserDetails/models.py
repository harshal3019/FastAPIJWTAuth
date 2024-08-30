from pydantic import BaseModel,EmailStr,Field,field_validator
from datetime import datetime

class UserDetailsModel(BaseModel):

   #  fullname:str
   #  email:EmailStr
   #  Designation:int
   #  Department:int
   #  Role:int
   #  Manager:str
   #  username: str = Field(min_length=3, max_length=20)
   #  password: str = Field(min_length=6, max_length=100)
   #  status: int = Field(default=1)  # Default value of 1
   fullname: str
   email: EmailStr
   Designation: int
   Department: int
   Role: int
   Manager: str
   user_details: int
   username: str = Field(min_length=3, max_length=20)
   password: str = Field(min_length=6, max_length=100)
   status: int = Field(default=1)
   created: datetime = Field(default_factory=datetime.now)
   status: int = Field(default=1)  # Default value of 1
    



@field_validator('status')
def check_status(cls, v):
   if v not in (0, 1):
      raise ValueError('Status must be 0 or 1')
   return v