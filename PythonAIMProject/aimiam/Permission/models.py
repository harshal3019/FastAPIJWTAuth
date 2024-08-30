from pydantic import BaseModel,Field,field_validator

class PermissionModel(BaseModel):
   permission_name:str
   permission_id:int
   category:str
   Type:str
   Module:str
   Description:str
   status: int = Field(default=1)  # Default value of 1

#to show or store only 0,1 value 
   @field_validator('status')
   def check_status(cls, v):
    if v not in (0, 1):
        raise ValueError('Status must be 0 or 1')
    return v

class updatePermissionModel(BaseModel):
   permission_name:str = None
   permission_id:int = None
   category:str = None
   Type:str = None
   Module:str = None
   Description:str = None
   status: int = Field(default=1)  # Default value of 1
