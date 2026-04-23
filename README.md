# 💰 Expense Tracker API (FastAPI)

A complete **Expense Tracker Backend Application** built using **FastAPI**.
This project includes **User Authentication with OTP**, **JWT Token System**, **Expense Management (CRUD)**, **Reports (Daily, Monthly, Category-wise)**, **Excel Export**, and **Automated Email Reports**.

---

## 🚀 Features

### 🔐 Authentication System

* User Registration
* Login with Email & Password
* OTP Verification (Email-based)
* JWT Token Generation (Access Token,Refresh token)
* Token Authenticate
* Secure Protected APIs

---

### 👤 User Flow

1. User registers
2. User logs in
3. OTP is sent to email
4. User verifies OTP
5. JWT Token is generated
6. Authenticate
7. User can access protected APIs

---

### 💸 Expense Management (CRUD)

* Create Expense
* Read All Expenses
* Read Single Expneses
* Update Expense
* Patch Expenses
* Delete Expense

Each expense includes:

* Title
* Amount
* Type (income/expense)
* Category
* Description
* Date
* Image (optional)

---

### 📊 Reports

* 📅 Daily Report
* 📆 Monthly Report
* 🗂 Category-wise Report
* 📋 All Expenses Report

---

### 📁 Excel Report

* Export all expenses to Excel file
* Category-wise and date-wise,Year wise structured data
* Downloadable `.xlsx` file
* Images shows

---

### 📧 Email Notifications

* Daily Expense Report via Email
* Monthly Expense Report via Email
* HTML-based Email with Table Format
* Includes Expense Details and Images

---

## 🛠 Tech Stack

* **Backend:** FastAPI
* **Database:** MySQL (via SQLAlchemy ORM)
* **Authentication:** JWT (OAuth2)
* **Email Service:** FastAPI-Mail (SMTP - Gmail)
* **Scheduler:** APScheduler
* **File Handling:** Static Files (Images)
* **Excel Export:** OpenPyXL

---

## 📂 Project Structure

```
expense_tracker/
│── main.py
│── database.py
│── models.py
│── schemas.py
│── dependencies.py
│── email_service.py
|--auth.py
│
├── routers/
│   ├── user.py
│   ├── expense.py
│   ├── report.py
│   ├── excelReport.py
│
├── media/                # Uploaded Images
├──.env
|--.gitignore
│
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/gyanvati-sahu/Expense_Tracker_App.git
cd expense-tracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Configure email credentials in `email_service.py`:

```python
MAIL_USERNAME = "your_email@gmail.com"
MAIL_PASSWORD = "your_app_password"
MAIL_FROM = "your_email@gmail.com"
```

👉 Use **App Password (not real password)**

---

## ▶️ Run the Server

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication APIs

| Method | Endpoint    | Description      |
| ------ | ----------- | ---------------- |
| POST   | /register   | Register user    |
| POST   | /login      | Login user       |
| POST   | /verify-otp | Verify OTP       |
| GET    | /me         | Get current user |

---

## 💸 Expense APIs

| Method | Endpoint     | Description      |
| ------ | ------------ | ---------------- |
| POST   | /create      | Create expense   |
| GET    | /expenses    | Get all expenses |
| PUT    | /update/{id} | Update expense   |
| PATCH  | /patch/{id}  | patch expenses   |
| GET    | /get/{id}    | get single expenses|

---

## 📊 Report APIs

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | /report/daily    | Daily report         |
| GET    | /report/monthly  | Monthly report       |
| GET    | /report/category | Category-wise report |
| GET    | /report/all      | All expenses         |

---

## 📁 Excel API

| Method | Endpoint        | Description           |
| ------ | --------------- | --------------------- |
| GET    | /download-excel | Download Excel report |

---

## 📧 Email APIs

| Method | Endpoint      | Description        |
| ------ | ------------- | ------------------ |
| GET    | /send-daily   | Send daily email   |
| GET    | /send-monthly | Send monthly email |

---

## ⏰ Scheduler Jobs

* Daily Report → Runs Automatically
* Monthly Report → Runs on 1st of every month

---

## 🖼 Image Handling

* Images are stored in `/media` folder
* Accessible via:

```
http://127.0.0.1:8000/media/<filename>
```

---

## ⚠️ Important Notes

* Email images require **public URL** (use ngrok or deployment)
* Use **App Password** for Gmail SMTP
* Ensure correct date format: `YYYY-MM-DD`

---

## 🎯 Future Enhancements

* Role-based Authentication (Admin/User)
* Dashboard UI (Frontend)
* Cloud Storage for Images (AWS S3 / Cloudinary)
* Pagination & Filtering
* Expense Analytics Graphs

---






