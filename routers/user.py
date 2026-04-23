from models import User
from fastapi import APIRouter,Depends,HTTPException
from schemas import UserCreate,UserLogin,OTPRequest
from dependencies import get_db
from sqlalchemy.orm import Session


from auth import hash_password,verify_password,create_access_token,create_refresh_token,get_current_user,otp_store,generate_otp

from email_service import send_otp_email
from auth import generate_otp, otp_store

from fastapi.security import OAuth2PasswordRequestForm

#email service
from email_service import send_otp_email

router=APIRouter()


#----register-----
@router.post("/register")
def register(user:UserCreate,db:Session=Depends(get_db)):
  db_user=User(
    name=user.name,
    email=user.email,
    password=hash_password(user.password),
    is_verified=False
  )

  db.add(db_user)
  db.commit()
  return {"msg":"User registered Successfully"}


#abhi jo kiya maine uska wala login mtlv esme token  generate nh ih
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    otp = generate_otp()
    otp_store[user.email] = otp

    await send_otp_email(user.email, otp)

    return {"msg": "OTP sent to email"}


#abhi wala jo access token verify password me hai
# @router.post("/verify-otp")
# def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):

#     user = db.query(User).filter(User.email == email).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if email not in otp_store:
#         raise HTTPException(status_code=400, detail="OTP not found")

#     if otp_store[email] != otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP")

#     user.is_verified = True
#     db.commit()

#     del otp_store[email]

#     access_token = create_access_token({"user_id": user.id})
#     refresh_token = create_refresh_token({"user_id": user.id})

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token
#     }


#extra
@router.post("/verify-otp")
def verify_otp(data: OTPRequest, db: Session = Depends(get_db)):

    email = data.email
    otp = data.otp

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if otp_store.get(email) != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    

    #imp
    user.is_verified=True
    db.commit()

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

  
##login



# @router.post("/login")
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):

#     # 🔥 username ko email treat karenge
#     db_user = db.query(User).filter(User.email == form_data.username).first()

#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if not verify_password(form_data.password, db_user.password):
#         raise HTTPException(status_code=400, detail="Invalid password")

#     access_token = create_access_token({
#         "user_id": db_user.id
#     })

#     refresh_token = create_refresh_token({
#         "user_id": db_user.id
#     })

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer"
#     }






#-----login----
# @router.post("/login")
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):

#     # username = email
#     db_user = db.query(User).filter(User.email == form_data.username).first()

#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if not verify_password(form_data.password, db_user.password):
#         raise HTTPException(status_code=400, detail="Invalid password")

#     # ❌ OTP NOT VERIFIED
#     if not db_user.is_verified:
#         raise HTTPException(
#             status_code=400,
#             detail="Please verify OTP first"
#         )

#     # ✅ ACCESS TOKEN
#     access_token = create_access_token({
#         "user_id": db_user.id,
#         "email": db_user.email
#     })

#     # ✅ REFRESH TOKEN
#     refresh_token = create_refresh_token({
#         "user_id": db_user.id
#     })

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer"
#     }


#it is used for token
# @router.post("/token")
# def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

#     user = db.query(User).filter(User.email == form_data.username).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if not verify_password(form_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Invalid password")

#     # OTP generate
#     otp = generate_otp()
#     otp_store[user.email] = otp

#     send_otp_email(user.email, otp)

#     return {"msg": "OTP sent"}