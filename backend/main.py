import smtplib
import os
from email.mime.text import MIMEText

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
from models import Student
import random
from dotenv import load_dotenv
import os
import requests
# create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv()


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# HOME ROUTE
# =====================================

@app.get("/")
def home():
    return {"message": "ARK Backend Running"}

# =====================================
# CHATBOT
# =====================================

class Message(BaseModel):
    text: str
    step: int
    name: str = ""

@app.post("/chat")
def chat(message: Message):

    if message.step == 0:
        return {
            "reply": "Hello! Welcome to ARK Analytics Academy 👋\nWhat is your name?",
            "step": 1,
            "name": ""
        }

    if message.step == 1:
        name = message.text
        return {
            "reply": f"Hi {name}! Are you a student or a working professional?",
            "step": 2,
            "name": name
        }

    if message.step == 2:
        name = message.name
        return {
            "reply": f"Nice to meet you {name}! 😊\n\nWe teach:\n• Python\n• Tableau\n• Power BI\n• SQL\n• Excel\n• Alteryx\n\nScan the QR code to enroll.",
            "step": 3,
            "name": name
        }

    if message.step == 3:
        return {
            "reply": "For details:\n📞 8309434566\n✉️ aabhilash712@gmail.com",
            "step": 4,
            "name": message.name
        }

    return {"reply": "Thank you!", "step": 4}

# =====================================
# OTP LOGIN SYSTEM
# =====================================

# =====================================
# OTP LOGIN SYSTEM (EMAIL VERSION)
# =====================================

class EmailRequest(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str

otp_store = {}

# function to send email OTP
def send_email_otp(to_email, otp):

    subject = "ARK Analytics Academy Login OTP"
    body = f"Your login OTP is: {otp}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_USER, EMAIL_PASS)

    server.sendmail(EMAIL_USER, to_email, msg.as_string())
    server.quit()


# SEND OTP (EMAIL)
@app.post("/send-otp")
def send_otp(data: EmailRequest):

    print("STEP 1: send-otp API called")

    db = SessionLocal()

    student = db.query(Student).filter(Student.email == data.email).first()

    if not student:
        print("STEP 2: student not found")
        db.close()
        return {"status": "access_denied"}

    print("STEP 3: student found")

    otp = str(random.randint(100000, 999999))

    otp_store[data.email] = otp

    print("STEP 4: OTP generated:", otp)

    send_email_otp(data.email, otp)

    print("STEP 5: OTP sent to email")

    db.close()

    return {"status": "otp_sent"}


# VERIFY OTP
@app.post("/verify-otp")
def verify_otp(data: OTPVerify):

    if data.email not in otp_store:
        return {"status": "invalid_otp"}

    if otp_store[data.email] != data.otp:
        return {"status": "invalid_otp"}

    db = SessionLocal()

    student = db.query(Student).filter(Student.email == data.email).first()

    if not student:
        db.close()
        return {"status": "access_denied"}

    db.close()

    return {
        "status": "success",
        "email": data.email
    }