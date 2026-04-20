import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

# Internal imports (Paths configured for the app structure)
from app.core.config import settings
from app.db.database import engine
from app.models.user import User

# OAuth2 setup: Defines where the client should send credentials to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Hashing Functions ---

def hash_password(password: str) -> str:
    """
    Converts a plain-text password into a secure hash.
    Truncates the input to 72 characters to handle Bcrypt's internal limit.
    """
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies whether the provided plain-text password matches the stored hash.
    """
    try:
        password_bytes = plain_password.encode('utf-8')[:72]
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

# --- Token Functions ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates a secure JWT (JSON Web Token) for the user.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# --- Dependency ---

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validates the token and extracts the details of the currently authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using the secret key and algorithm defined in settings
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    with Session(engine) as session:
        # Fetch the user from the database based on the email stored in the token
        user = session.exec(select(User).where(User.email == email)).first()
        if user is None:
            raise credentials_exception
        return user