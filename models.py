from database import Base

from sqlalchemy import Integer,String,Column,ForeignKey,Date,Boolean
from sqlalchemy.orm import relationship


class User(Base):
  __tablename__="users"

  id=Column(Integer,primary_key=True)
  name=Column(String(100))
  email=Column(String(200),unique=True)
  password=Column(String(200))

  expenses=relationship("Expense",back_populates="owner")
  is_verified = Column(Boolean, default=False)


class Expense(Base):
  __tablename__="expenses"

  id=Column(Integer,primary_key=True)
  title=Column(String(100))
  amount=Column(Integer)
  type=Column(String(50))
  category=Column(String(100))
  description=Column(String(255))
  date=Column(Date)
  image = Column(String(255), nullable=True)  

  user_id=Column(Integer,ForeignKey("users.id"))
  owner=relationship("User",back_populates="expenses")
