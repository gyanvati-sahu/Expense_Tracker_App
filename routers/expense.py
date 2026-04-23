from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form,HTTPException
from sqlalchemy.orm import Session

from models import Expense,User
from schemas import ExpenseCreate,ExpenseUpdate,ExpenseResponse
from dependencies import get_db
from auth import get_current_user
from fastapi import UploadFile, File
import shutil
import os
import uuid

router=APIRouter()

# @router.post("/create")
# def create_expense(
#     expense: ExpenseCreate,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     new_expense = Expense(
#         title=expense.title,
#         amount=expense.amount,
#         type=expense.type,
#         category=expense.category,
#         description=expense.description,
#         date=expense.date,
#         images=expense.image,
#         user_id=current_user.id
#     )

#     db.add(new_expense)
#     db.commit()
#     db.refresh(new_expense)

#     return new_expense
UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/create")
def create_expense(
    title: str = Form(...),
    amount: int = Form(...),
    type: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    file: UploadFile = File(...),   # ✅ image allowed
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not file:
        raise HTTPException(status_code=400, detail="Image is required")

    file_name = f"{uuid.uuid4()}_{file.filename}"
    # file_path = os.path.join(UPLOAD_DIR, file_name)
    file_path = os.path.join("media", file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_expense = Expense(
        title=title,
        amount=amount,
        type=type,
        category=category,
        description=description,
        date=date,
        image=file_path,   # ✅ image stored
        user_id=current_user.id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

#get

@router.get("/read")
def read_expenses(db:Session=Depends(get_db),
                  user:User=Depends(get_current_user)):
    return db.query(Expense).filter(Expense.user_id==user.id).all()


#update
@router.put("/update/{id}")
def update_expense(
    id: int,
    title: str = Form(...),
    amount: int = Form(...),
    type: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    file: UploadFile = File(None),   # ✅ optional image
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    data = db.query(Expense).filter(
        Expense.id == id,
        Expense.user_id == user.id
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail="Not found")

    data.title = title
    data.amount = amount
    data.type = type
    data.category = category
    data.description = description
    data.date = date

    # ✅ image update logic
    if file:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data.image = file_path

    db.commit()
    db.refresh(data)

    return data


# ➤ DELETE EXPENSE
import os

@router.delete("/{id}")
def delete_expense(id: int,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):

    data = db.query(Expense).filter(
        Expense.id == id,
        Expense.user_id == user.id
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail="Not found")

    # ✅ delete image from folder
    if data.image and os.path.exists(data.image):
        os.remove(data.image)

    db.delete(data)
    db.commit()

    return {"msg": "Deleted successfully"}

    

#get single daata read
@router.get("/read_single/{id}")
def get_expense(id: int,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):

    data = db.query(Expense).filter(
        Expense.id == id,
        Expense.user_id == user.id
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail="Not found")

    return data

#patch  method updated single data
@router.patch("/patch/{id}")
def patch_expense(
    id: int,
    title: str = Form(None),
    amount: int = Form(None),
    type: str = Form(None),
    category: str = Form(None),
    description: str = Form(None),
    date: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    data = db.query(Expense).filter(
        Expense.id == id,
        Expense.user_id == user.id
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail="Not found")

    if title:
        data.title = title
    if amount:
        data.amount = amount
    if type:
        data.type = type
    if category:
        data.category = category
    if description:
        data.description = description
    if date:
        data.date = date

    # ✅ image optional patch
    if file:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data.image = file_path

    db.commit()
    db.refresh(data)

    return data