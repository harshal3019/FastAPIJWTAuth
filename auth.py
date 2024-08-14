from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "HL6uRxS9GjYgkcJyASyIwG-XI80EKHf1w8NwWVlYiv8="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    from bcrypt import checkpw
    return checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password):
    from bcrypt import hashpw, gensalt
    return hashpw(password.encode('utf-8'), gensalt())

