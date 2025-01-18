from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    """
    This function will return the user id from the JWT token.
    """
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        id: int = payload.get("sub")
        if id is None:
            raise credentials_exception
    except:
        raise credentials_exception
    return id
