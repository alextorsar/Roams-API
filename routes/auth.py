
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.user import UserCreate, UserResponse, UserLogin
from models.user import User
from core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )
    else:
        hasehd_password = hash_password(user.password)
        new_user = User(
            name=user.name,
            email=user.email,
            password=hasehd_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

@router.post("/login", response_model=dict)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    database_user = db.query(User).filter(User.email == user.email).first()
    if not database_user or not verify_password(user.password, database_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    else:
        access_token = create_access_token(data={"sub": database_user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    
    
