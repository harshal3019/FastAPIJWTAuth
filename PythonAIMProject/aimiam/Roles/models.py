from pydantic import BaseModel,field_validator,Field

class RolesModel(BaseModel):
   role_name : str
   role_id : int
   description : str
   status: int = Field(default=1)  # Default value of 1

#to show or store only 0,1 value 
   @field_validator('status')
   def check_status(cls, v):
    if v not in (0, 1):
        raise ValueError('Status must be 0 or 1')
    return v
   
class UpdateRolesModel(BaseModel):
    role_name : str = None
    role_id : int = None
    description : str = None
    status: int = Field(default=1) # Default value of 