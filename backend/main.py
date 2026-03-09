from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
@app.get("/")
def home():
    return {"message": "ARK Chatbot Backend Running"}

class Message(BaseModel):
    text: str
    step: int
    name: str = ""

@app.post("/chat")
def chat(message: Message):

    user_text = message.text.lower()

    # STEP 0 → Greeting
    if message.step == 0:
        return {
            "reply": "Hello! Welcome to ARK Analytics Academy 👋\nWhat is your name?",
            "step": 1,
            "name": ""
        }

    # STEP 1 → Ask name
    if message.step == 1:
        name = message.text
        return {
            "reply": f"Hi {name}! Are you a student or a working professional?",
            "step": 2,
            "name": name
        }

    # STEP 2 → Ask student or professional
    if message.step == 2:
        name = message.name

        return {
            "reply": f"Nice to meet you {name}! 😊\n\nWe teach the following courses:\n\n• Python\n• Tableau\n• Power BI\n• SQL\n• Excel\n• Alteryx\n\nPlease scan the QR code on this page to enroll.",
            "step": 3,
            "name": name
        }

    # STEP 3 → Final message
    if message.step == 3:
        return {
            "reply": "For further details:\n📞 Call: 8309434566\n✉️ Email: aabhilash712@gmail.com\n\nWe look forward to helping you learn data analytics!",
            "step": 4,
            "name": message.name
        }

    return {"reply": "Thank you for contacting ARK Analytics Academy!", "step": 4}