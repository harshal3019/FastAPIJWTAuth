from pydantic import BaseModel

class DesignationModel(BaseModel):
   designation_name:str
   id:int

class UpdateDesignationModel(BaseModel):
   designation_name: str = None