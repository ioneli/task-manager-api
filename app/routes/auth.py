from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password, verify_password, create_token
from app.schemas.user import UserCreate, UserLogin

from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()

def get_db():
 db = SessionLocal()
 try:
  yield db
 finally:
  db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
 new_user = User(
  email=user.email,
  password=hash_password(user.password)
 )

 db.add(new_user)
 db.commit()

 return{"message":"user created"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        return {"error": "invalid credentials"}

    if not verify_password(form_data.password, db_user.password):
        return {"error": "invalid credentials"}

    token = create_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
