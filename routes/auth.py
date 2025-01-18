
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.user import UserCreate, UserResponse
from core.security import verify_password, create_access_token
from services.user import get_user_by_email, create_new_user

router = APIRouter()

@router.post("/register/", response_model=UserResponse, summary="Register a new user")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
        This endpoint is used to register a new user. It should receive a UserCreate schema with this fields:\n
        - **name**: The name of the user\n
        - **email**: The email of the user\n
        - **password**: The password of the user\n
        It will return a UserResponse schema.
    """
    if get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )
    else:
        new_user = create_new_user(user.password, user.name, user.email, db)
    return new_user

@router.post("/login/", response_model=dict, summary="Login a user")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    This endpoint is used to log in a user. It should receive data in **form-data** or **x-www-form-urlencoded** format with the following fields:\n
    - **username**: The email of the user\n
    - **password**: The password of the user\n
    It will return a bearer token that should be used to authenticate the user in other endpoints.
    """
    database_user = get_user_by_email(form_data.username, db)
    if not database_user or not verify_password(form_data.password, database_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": str(database_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}