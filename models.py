# models.py

from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6, max_length=100)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFtbGkiLCJleHAiOjE3MjM2MTg2NDV9.BGH2W_v18dFSN_k8yt7ioZjSOoqz9s7aJ5mMXGzZEM8