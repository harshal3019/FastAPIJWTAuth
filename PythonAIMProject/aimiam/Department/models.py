from pydantic import BaseModel,field_validator,Field

class DepartmentModel(BaseModel):
   department_name : str
   dept_id : int
   status: int = Field(default=1)  # Default value of 1

#to show or store only 0,1 value 
   @field_validator('status')
   def check_status(cls, v):
    if v not in (0, 1):
        raise ValueError('Status must be 0 or 1')
    return v
   
class UpdateDepartmentModel(BaseModel):
      department_name : str = None
      status : int = Field(default=1)
