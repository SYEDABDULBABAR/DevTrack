from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.user import User, UserBase
from app.core.security import hash_password, verify_password, create_access_token 
from typing import Optional

# Alag se UserCreate class yahan define kar rahe hain agar user.py mein nahi hai
class UserCreate(UserBase):
    password: str

# Router setup
router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- 1. USER REGISTRATION ENDPOINT ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # 1. Check karein agar email pehle se database mein hai
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Yeh email pehle se register hai."
        )

    # 2. Password hash karein aur naya User object banayein
    hashed_pwd = hash_password(user_data.password)
    
    # User model create karein (password field ko hash se replace karke)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
        )
    
    return {
        "status": "success",
        "message": "User registered successfully", 
        "user_id": new_user.id
    }

# --- 2. USER LOGIN ENDPOINT (JWT Generation) ---
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
):
    # Step 1: User ko email ke zariye dhoondo (OAuth2 mein username hi email hota hai)
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()

    # Step 2: Password verify karein
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ya password galat hai",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 3: Access Token generate karein
    access_token = create_access_token(data={"sub": user.email})

    # Step 4: Token return karein
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id 
    }