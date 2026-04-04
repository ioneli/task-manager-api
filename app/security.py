from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(
 schemes=["bcrypt"],
 deprecated="auto"
 )

def hash_password(password: str):
 return pwd_context.hash(password)

def verify_password(password: str, hashed):
 return pwd_context.verify(password, hashed)

def create_token(data: dict):

 to_encode = data.copy()

 expire = datetime.utcnow() + timedelta(hours=2)

 to_encode.update({"exp":expire})

 encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

 return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

 token = credentials.credentials

 try:
  payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

  user_id = payload.get("user_id")

  if user_id is None:
   raise HTTPException(status_code=401, detail="invalid token")

  return user_id

 except JWTError:
  raise HTTPException(status_code=401, detail="invalid token")
 
