from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.user import User
from app.core.config import settings  # Retrieving SECRET_KEY and ALGORITHM from settings

# This line enables the 'Authorize' button in the Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    session: Session = Depends(get_session)
) -> User:
    # Standard 401 Error for Unauthorized access
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the JWT token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        # Extract email from the 'sub' (subject) claim in the token
        email: str = payload.get("sub") 
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # 2. Verify the user exists in the database
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception
        
    return user