from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.user import User
from app.core.config import settings # Apne settings se SECRET_KEY aur ALGORITHM lein

# Ye line Swagger UI mein 'Authorize' button activate karti hai
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    session: Session = Depends(get_session)
) -> User:
    # 401 Error for Unauthorized access (Requirement ke mutabiq)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Token decode karein
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub") # Token mein sub (subject) email hota hai
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # 2. Database mein user ko check karein
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if user is None:
        raise credentials_exception
        
    return user