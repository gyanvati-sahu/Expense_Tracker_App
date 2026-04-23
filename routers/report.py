from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from datetime import datetime
from dependencies import get_db
from models import Expense,User
from auth import get_current_user
from typing import Optional
from datetime import date


router=APIRouter()

#all report api in single api
@router.get("/full-report")
def full_report(
    year: Optional[int] = None,
    month: Optional[int] = None,
    category: Optional[str] = None,

    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    
    
    user: User = Depends(get_current_user)
):
    query = db.query(Expense).filter(Expense.user_id == user.id)

    

    if year:
        query = query.filter(Expense.date >= date(year, 1, 1),
                             Expense.date <= date(year, 12, 31))

    if month:
        query = query.filter(Expense.date >= date(datetime.now().year, month, 1),
                             Expense.date <= date(datetime.now().year, month, 28))

    if start_date and end_date:
        query = query.filter(Expense.date >= start_date,
                             Expense.date <= end_date)
        
    if category:
        query = query.filter(Expense.category == category)

    
    expenses = query.all()
   

    #TOTAL
    total = sum(exp.amount for exp in expenses)

    #DAY WISE
    day_data = {}
    for exp in expenses:
        day = exp.date.strftime("%Y-%m-%d")
        day_data[day] = day_data.get(day, 0) + exp.amount

    #MONTHLY
    month_data = {}
    for exp in expenses:
        month = exp.date.strftime("%Y-%m")
        month_data[month] = month_data.get(month, 0) + exp.amount

    #CATEGORY
    category_data = {}
    for exp in expenses:
        category_data[exp.category] = category_data.get(exp.category, 0) + exp.amount

    #ALL EXPENSES
    all_data = []
    for exp in expenses:
        all_data.append({
            "title": exp.title,
            "amount": exp.amount,
            "type": exp.type,
            "category": exp.category,
            "description": exp.description,
            "date": exp.date.strftime("%Y-%m-%d")
        })

    return {
        "user_id": user.id,
        "total_expenses": total,
        "daily_report": day_data,
        "monthly_report": month_data,
        "category_report": category_data,
        "all_expenses": all_data
    }


#send mail fun
def get_user_report_data(expenses):

    # Day wise
    day_data = {}
    for exp in expenses:
        day = exp.date.strftime("%Y-%m-%d")
        day_data[day] = day_data.get(day, 0) + exp.amount

    # Monthly
    month_data = {}
    for exp in expenses:
        month = exp.date.strftime("%Y-%m")
        month_data[month] = month_data.get(month, 0) + exp.amount

    # Category wise
    category_data = {}
    for exp in expenses:
        category_data[exp.category] = category_data.get(exp.category, 0) + exp.amount

    return day_data, month_data, category_data
