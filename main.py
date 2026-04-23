from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, SessionLocal
from models import Base, User, Expense

from routers import user, expense, report, excelReport
from email_service import send_expense_email
from routers.report import get_user_report_data

from datetime import datetime
import asyncio
import time
from openpyxl.drawing.image import Image as ExcelImage
from PIL import Image as PILImage

# scheduler.start()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, SessionLocal
from models import Base, User, Expense
from email_service import send_expense_email

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

app = FastAPI()
from fastapi.staticfiles import StaticFiles

app.mount("/media", StaticFiles(directory="media"), name="media")
# Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(expense.router)
app.include_router(report.router)
app.include_router(excelReport.router)

Base.metadata.create_all(bind=engine)

app.mount("/media", StaticFiles(directory="media"), name="media")

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()

BASE_URL = "http://127.0.0.1:8000"

# =====================================================
# 🔥 COMMON HTML BUILDER (Excel-like table)
# =====================================================
def build_html(user, expenses, title):

    body = f"""
    <html>
    <body style="font-family:Arial;">

    <h2>👋 Hello {user.name}</h2>
    <h3>📊 {title}</h3>

    <table border="1" cellpadding="8" cellspacing="0"
    style="border-collapse:collapse; width:100%; text-align:center;">

    <tr style="background:#f2f2f2;">
        <th>Title</th>
        <th>Amount</th>
        <th>Type</th>
        <th>Category</th>
        <th>Description</th>
        <th>Date</th>
        <th>Image</th>
    </tr>
    """

    for exp in expenses:

        image_url = f"{BASE_URL}/{exp.image}" if exp.image else ""

        img_tag = f"""
        <img src="{image_url}" width="80" height="80"
        style="border-radius:8px;" />
        """ if exp.image else "No Image"

        body += f"""
        <tr>
            <td>{exp.title}</td>
            <td>{exp.amount}</td>
            <td>{exp.type}</td>
            <td>{exp.category}</td>
            <td>{exp.description}</td>
            <td>{exp.date}</td>
            <td>{img_tag}</td>
        </tr>
        """

    body += """
    </table>

    <p style="margin-top:20px;font-size:12px;color:gray;">
    Auto generated Expense Report
    </p>

    </body>
    </html>
    """

    return body


def process_daily_report():

    print("🔥 Running DAILY report")

    import asyncio
    import os
    from datetime import datetime
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image as ExcelImage

    db = SessionLocal()
    users = db.query(User).filter(User.is_verified == True).all()

    today_str = datetime.now().strftime("%Y-%m-%d")

    for user in users:

        expenses = db.query(Expense).filter(
            Expense.user_id == user.id
        ).all()

        daily_expenses = []

        for exp in expenses:

            if not exp.date:
                continue

            try:
                if isinstance(exp.date, str):
                    exp_date_str = exp.date[:10]
                else:
                    exp_date_str = exp.date.strftime("%Y-%m-%d")

                if exp_date_str == today_str:
                    daily_expenses.append(exp)

            except Exception as e:
                print("DATE ERROR:", e)
                continue

        print("USER:", user.email, "DAILY COUNT:", len(daily_expenses))

        if not daily_expenses:
            print("NO DAILY DATA:", user.email)
            continue

        rows = ""
        image_attachments = []

        # ================= EXCEL CREATE =================
        excel_file = f"daily_report_{user.id}.xlsx"

        wb = Workbook()
        ws = wb.active
        ws.title = "Daily Report"

        # 👉 Add Image column
        ws.append(["Title", "Amount", "Type", "Category", "Description", "Date", "Image"])

        row_num = 2  # Excel row tracking

        # ================= LOOP =================
        for exp in daily_expenses:

            ws.append([
                exp.title,
                exp.amount,
                exp.type,
                exp.category,
                exp.description,
                str(exp.date),
                ""  # empty for image column
            ])

            img_tag = "No Image"

            if exp.image:

                clean_path = exp.image.replace("media\\", "").replace("media/", "")
                full_path = os.path.abspath(os.path.join("media", clean_path))

                cid = f"img_{exp.id}"

                if os.path.exists(full_path):

                    # ===== EMAIL IMAGE =====
                    img_tag = f'<img src="cid:{cid}" width="80" height="80"/>'
                    image_attachments.append((cid, full_path))

                    print("🖼 IMAGE FOUND:", full_path)

                    # ===== EXCEL IMAGE =====
                    try:
                        img = ExcelImage(full_path)
                        img.width = 50
                        img.height = 50

                        ws.row_dimensions[row_num].height = 60
                        ws.column_dimensions["G"].width = 20

                        ws.add_image(img, f"G{row_num}")

                        print("✅ IMAGE ADDED TO EXCEL")

                    except Exception as e:
                        print("❌ EXCEL IMAGE ERROR:", e)

                else:
                    print("❌ IMAGE NOT FOUND:", full_path)

            rows += f"""
            <tr>
                <td>{exp.title}</td>
                <td>{exp.amount}</td>
                <td>{exp.type}</td>
                <td>{exp.category}</td>
                <td>{exp.description}</td>
                <td>{exp.date}</td>
                <td>{img_tag}</td>
            </tr>
            """

            row_num += 1

        # SAVE EXCEL
        wb.save(excel_file)
        print("📁 EXCEL CREATED:", excel_file)

        # ================= EMAIL BODY =================
        body = f"""
        <html>
        <body>

        <h2>👋 Hello {user.name}</h2>
        <h3>📊 Daily Expense Report ({today_str})</h3>

        <table border="1" cellpadding="8" cellspacing="0">

        <tr>
            <th>Title</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Category</th>
            <th>Description</th>
            <th>Date</th>
            <th>Image</th>
        </tr>

        {rows}

        </table>

        </body>
        </html>
        """

        # ================= SEND EMAIL =================
        try:
            asyncio.run(
                send_expense_email(
                    user.email,
                    "📊 Daily Expense Report",
                    body,
                    image_attachments,
                    excel_file
                )
            )

            print("✅ DAILY EMAIL SENT:", user.email)

        except Exception as e:
            print("❌ EMAIL ERROR:", e)

    db.close()


def process_monthly_report():

    print("🔥 Running MONTHLY report")

    import asyncio
    import os
    from datetime import datetime
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image as ExcelImage

    db = SessionLocal()
    users = db.query(User).filter(User.is_verified == True).all()

    current_month = datetime.now().strftime("%Y-%m")

    for user in users:

        expenses = db.query(Expense).filter(
            Expense.user_id == user.id
        ).all()

        # ✅ MONTH FILTER
        month_expenses = []

        for exp in expenses:
            if not exp.date:
                continue

            try:
                if isinstance(exp.date, str):
                    exp_month = exp.date[:7]
                else:
                    exp_month = exp.date.strftime("%Y-%m")

                if exp_month == current_month:
                    month_expenses.append(exp)

            except Exception as e:
                print("DATE ERROR:", e)
                continue

        print("USER:", user.email, "MONTH COUNT:", len(month_expenses))

        if not month_expenses:
            print("NO MONTH DATA:", user.email)
            continue

        rows = ""
        image_attachments = []

        # ================= EXCEL CREATE =================
        excel_file = f"monthly_report_{user.id}.xlsx"

        wb = Workbook()
        ws = wb.active
        ws.title = "Monthly Report"

        ws.append(["Title", "Amount", "Type", "Category", "Description", "Date", "Image"])

        row_num = 2

        # ================= LOOP =================
        for exp in month_expenses:

            ws.append([
                exp.title,
                exp.amount,
                exp.type,
                exp.category,
                exp.description,
                str(exp.date),
                ""
            ])

            img_tag = "No Image"

            if exp.image:

                clean_path = exp.image.replace("media\\", "").replace("media/", "")
                full_path = os.path.abspath(os.path.join("media", clean_path))

                cid = f"img_{exp.id}"

                if os.path.exists(full_path):

                    # ===== EMAIL IMAGE =====
                    img_tag = f'<img src="cid:{cid}" width="80" height="80"/>'
                    image_attachments.append((cid, full_path))

                    print("🖼 IMAGE FOUND:", full_path)

                    # ===== EXCEL IMAGE =====
                    try:
                        img = ExcelImage(full_path)
                        img.width = 50
                        img.height = 50

                        ws.row_dimensions[row_num].height = 60
                        ws.column_dimensions["G"].width = 20

                        ws.add_image(img, f"G{row_num}")

                        print("✅ IMAGE ADDED TO EXCEL")

                    except Exception as e:
                        print("❌ EXCEL IMAGE ERROR:", e)

                else:
                    print("❌ IMAGE NOT FOUND:", full_path)

            rows += f"""
            <tr>
                <td>{exp.title}</td>
                <td>{exp.amount}</td>
                <td>{exp.type}</td>
                <td>{exp.category}</td>
                <td>{exp.description}</td>
                <td>{exp.date}</td>
                <td>{img_tag}</td>
            </tr>
            """

            row_num += 1

        # SAVE EXCEL
        wb.save(excel_file)
        print("📁 EXCEL CREATED:", excel_file)

        # ================= EMAIL BODY =================
        body = f"""
        <html>
        <body>

        <h2>👋 Hello {user.name}</h2>
        <h3>📊 Monthly Expense Report ({current_month})</h3>

        <table border="1" cellpadding="8" cellspacing="0">

        <tr>
            <th>Title</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Category</th>
            <th>Description</th>
            <th>Date</th>
            <th>Image</th>
        </tr>

        {rows}

        </table>

        </body>
        </html>
        """

        # ================= SEND EMAIL =================
        try:
            asyncio.run(
                send_expense_email(
                    user.email,
                    "📊 Monthly Expense Report",
                    body,
                    image_attachments,
                    excel_file
                )
            )

            print("✅ MONTHLY EMAIL SENT:", user.email)

        except Exception as e:
            print("❌ EMAIL ERROR:", e)

    db.close()


# =====================================================
# 🔥 API ENDPOINTS
# =====================================================
@app.get("/send-daily")
def send_daily():
    process_daily_report()
    return {"message": "Daily email sent successfully"}


@app.get("/send-monthly")
def send_monthly():
    process_monthly_report()
    return {"message": "Monthly email sent successfully"}


# =====================================================
# 🔥 SCHEDULER
# =====================================================
scheduler.add_job(process_daily_report, "interval", minutes=1)
scheduler.add_job(process_monthly_report, "cron", day=1, hour=10)

scheduler.start()