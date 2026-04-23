from pydantic import BaseModel
from datetime import date


class UserCreate(BaseModel):
  name:str
  email:str
  password:str


class UserLogin(BaseModel):
  email:str
  password:str


class ExpenseCreate(BaseModel):
  title:str
  amount:int
  type:str
  category:str
  description:str
  date:date

class ExpenseUpdate(BaseModel):
    title: str
    amount: int
    type: str
    category: str
    description: str
    date: date
    

class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: int
    type: str
    category: str
    description: str
    date: date
    user_id: int

    class Config:
        from_attributes = True


class OTPRequest(BaseModel):
   email:str
   otp:str