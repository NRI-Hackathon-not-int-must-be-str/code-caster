from app.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization")


def verify_token(auth_header: str = Depends(api_key_header)):
    if auth_header != settings.TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization Error",
        )
