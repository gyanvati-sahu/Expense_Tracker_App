from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import mimetypes

conf = ConnectionConfig(
    MAIL_USERNAME="gyansahu202@gmail.com",
    MAIL_PASSWORD="yjhszcqkstgekmkx",
    MAIL_FROM="gyansahu202@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)

async def send_otp_email(email: str, otp: str):
    message = MessageSchema(
        subject="OTP Verification",
        recipients=[email],
        body=f"Your OTP is: {otp}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)





# async def send_expense_email(email: str, subject: str, body: str):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email],
#         body=body,
#         subtype="html"   # 🔥 IMPORTANT FIX (not plain)
#     )

#     await fm.send_message(message)

# ================= EXPENSE EMAIL (FIXED VERSION) =================
# ================= EXPENSE EMAIL (FINAL) =================
# ================= EXPENSE EMAIL =================
SENDER_EMAIL = "gyansahu202@gmail.com"
SENDER_PASSWORD = "yjhszcqkstgekmkx"


async def send_expense_email(email, subject, body, image_attachments=None, excel_file=None):

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    # HTML BODY
    msg.attach(MIMEText(body, "html"))

    # ================= IMAGES (FIXED) =================
    if image_attachments:
        for cid, path in image_attachments:

            if os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        img_data = f.read()

                    mime_type, _ = mimetypes.guess_type(path)

                    if mime_type:
                        subtype = mime_type.split("/")[-1]
                    else:
                        subtype = "png"  # fallback

                    img = MIMEImage(img_data, _subtype=subtype)

                    img.add_header("Content-ID", f"<{cid}>")
                    img.add_header("Content-Disposition", "inline")

                    msg.attach(img)

                    print("✅ IMAGE ATTACHED:", path)

                except Exception as e:
                    print("❌ IMAGE ERROR:", e)

    # ================= EXCEL ATTACH =================
    if excel_file and os.path.exists(excel_file):
        with open(excel_file, "rb") as f:
            part = MIMEApplication(f.read(), _subtype="xlsx")
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(excel_file)}"'
            )
            msg.attach(part)

        print("📎 EXCEL ATTACHED:", excel_file)

    # ================= SEND =================
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print("✅ EMAIL SENT SUCCESSFULLY:", email)

    except Exception as e:
        print("❌ EMAIL SEND ERROR:", e)


