from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import pathlib
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_KEY = os.getenv("CLIENT_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication

def validate_token(api_key: str = Depends(oauth2_scheme)):
    if api_key != CLIENT_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )