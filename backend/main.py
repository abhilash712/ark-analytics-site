import resend
import os


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

resend.api_key = os.getenv("RESEND_API_KEY")


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

# =====================================
# CHATBOT
# =====================================

class Message(BaseModel):
    text: str
    step: int
    name: str = ""

@app.post("/chat")
def chat(message: Message):

    question = message.text.lower()

    # ------------------------------
    # BASIC QUESTIONS
    # ------------------------------

    if "course" in question or "what do you teach" in question:
        return {
            "reply": "We teach industry tools including Python, SQL, Tableau, Power BI, Alteryx and Advanced Excel.",
            "step": message.step,
            "name": message.name
        }

    if "python" in question:
        return {
            "reply": "Python is a programming language used for data analysis, automation and machine learning. In our course you will learn Python basics and data analysis projects.",
            "step": message.step,
            "name": message.name
        }

    if "sql" in question:
        return {
            "reply": "SQL stands for Structured Query Language. It is used to analyze and manage data stored in databases.",
            "step": message.step,
            "name": message.name
        }

    if "tableau" in question:
        return {
            "reply": "Tableau is a data visualization tool used to build dashboards and interactive reports.",
            "step": message.step,
            "name": message.name
        }

    if "power bi" in question:
        return {
            "reply": "Power BI is a Microsoft business intelligence tool used to create dashboards and analyze business data.",
            "step": message.step,
            "name": message.name
        }

    if "alteryx" in question:
        return {
            "reply": "Alteryx is a data analytics automation platform used for data preparation and workflow automation.",
            "step": message.step,
            "name": message.name
        }

    if "mentor" in question or "who teaches" in question:
        return {
            "reply": "Our mentor is an experienced Data Analytics professional currently working as a Data Analyst Team Lead at JP Morgan Chase. She has strong experience in Python, SQL, Tableau, Power BI and Alteryx automation.",
            "step": message.step,
            "name": message.name
        }

    if "enroll" in question or "join" in question:
        return {
            "reply": "You can scan the QR code on this page to enroll in ARK Analytics Academy.",
            "step": message.step,
            "name": message.name
        }

    if "contact" in question or "phone" in question:
        return {
            "reply": "For more details please contact ARK Analytics Academy. Phone: 8309434566 Email: aabhilash712@gmail.com",
            "step": message.step,
            "name": message.name
        }

    # ------------------------------
    # STEP CONVERSATION
    # ------------------------------

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
            "reply": "For more information please contact ARK Analytics Academy.\n📞 8309434566\n✉️ aabhilash712@gmail.com",
            "step": 4,
            "name": message.name
        }

    # ------------------------------
    # FALLBACK
    # ------------------------------

    return {
        "reply": "Sorry, I couldn't understand that question.\n\nPlease contact ARK Analytics Academy.\n📞 8309434566\n✉️ aabhilash712@gmail.com",
        "step": message.step,
        "name": message.name
    }

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

    params = {
        "from": "ARK Analytics <onboarding@resend.dev>",
        "to": [to_email],
        "subject": "ARK Analytics Academy Login OTP",
        "html": f"""
        <h2>Your OTP is: {otp}</h2>
        <p>Use this code to login to ARK Analytics Academy.</p>
        <p>This OTP will expire soon.</p>
        """
    }

    resend.Emails.send(params)


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