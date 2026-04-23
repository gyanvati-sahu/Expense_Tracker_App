  
from dependencies import get_db
from passlib.context import CryptContext

from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from models import User
from jose import jwt,JWTError
from datetime import datetime,timedelta

from config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS


# SECRET_KEY="mysecretkey"
# ALGORITHM="HS256"

# oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ FIXED



def hash_password(password: str):
    password = password.strip()[:72]   # ✅ trim + limit
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain.strip()[:72], hashed)


#access token
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp":expire,
        "type":"access"
    })

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


#refresh token
def create_refresh_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp":expire,
        "type":"refresh"
    })

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    

 



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials   # ✅ extract token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


otp_store = {}

def generate_otp():
    import random
    return str(random.randint(100000, 999999))
