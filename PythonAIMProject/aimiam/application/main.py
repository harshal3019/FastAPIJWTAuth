from fastapi import FastAPI, Depends, HTTPException, status,BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId
from application.models import UserCreate, Token
from application.auth import create_access_token, verify_password, get_password_hash,SECRET_KEY,ALGORITHM
from application.database import user_collections
from pydantic import BaseModel
from typing import Any
import json
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from application.forms import CustomLoginForm
from application.Setting import FastMail, MessageSchema,conf,EmailStr
from Designation.routes import designation_root
from Department.routes import department_root
from Roles.routes import roles_root
from Permission.routes import permission_root
from UserDetails.routes import userdetails_root
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def object_id_str(document: dict) -> dict:
    """Convert ObjectId to string for MongoDB documents."""
    document["_id"] = str(document["_id"])
    return document




async def send_registration_email(email: EmailStr, username: str, password: str):
    message = MessageSchema(
        subject="Welcome to Our Service",
        recipients=[email],
        body=f"""
        Hi {username},
        Welcome to our service! Here are your login details:

        Username: {username}
        Password: {password}

        Please keep this information safe.
        """,
        subtype="plain"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)

@app.post("/register", response_model=Token)
async def register(user: UserCreate, background_tasks: BackgroundTasks):
    try:
        # Check if the email or username is already registered
        if user_collections.find_one({"email": user.email}) or user_collections.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="Email or username already registered")

        # Store the original password before hashing
        original_password = user.password

        # Hash the password and insert the user into the database
        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user.password)
        result = user_collections.insert_one(user_dict)

        # Send registration email with the original password (without hash)
        background_tasks.add_task(send_registration_email, user.email, user.username, original_password)

        # Generate an access token
        access_token = create_access_token(data={"sub": user.username})

        # Return the response with a status code and message
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "status": "ok",
                "msg": "User registered successfully"
            }
        )
    except Exception as e:
        print(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    



@app.post("/refreshtoken", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(CustomLoginForm.as_form)):
    try:
        user = user_collections.find_one({"username": form_data.username})
        if not user or not verify_password(form_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = user_collections.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        return object_id_str(user)  # Convert ObjectId to string
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception as e:
        print(f"Error during user retrieval: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

app.include_router(designation_root)
app.include_router(department_root)
app.include_router(roles_root)
app.include_router(permission_root)
app.include_router(userdetails_root)