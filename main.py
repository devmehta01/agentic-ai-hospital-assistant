from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nodes.intent_node import classify_intent
from nodes.intake_node import extract_intake_details

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Store user memory temporarily (single user for now)
user_memory = {
    "intent": None,
    "awaiting_intake": False
}

@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message
    memory = user_memory

    # If we're waiting for intake details
    if memory["awaiting_intake"]:
        try:
            intake = extract_intake_details(message)
            memory["intake_details"] = intake
            memory["awaiting_intake"] = False

            return {
                "reply": f"Thanks {intake['name']}! Based on your symptoms ({intake['symptoms']}), I’ll now help you find the right doctor."
            }
        except Exception:
            return {
                "reply": "Sorry, I couldn’t understand that. Please provide your full name, driver license number, and a brief description of your symptoms."
            }

    # Detect intent
    intent = classify_intent(message)
    memory["intent"] = intent

    if intent == "book_appointment":
        memory["awaiting_intake"] = True
        return {
            "reply": "Got it. Please provide your full name, driver license number, and a brief description of your symptoms."
        }

    # Other intents can be handled similarly
    return {
        "reply": f"I detected your intent as: **{intent}**. (This is a placeholder response.)"
    }
