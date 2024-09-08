from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import authenticate_user, create_access_token, get_current_user
from database import get_db
from models import User
from schemas import UserCreate, MessageCreate, Token
from crud import create_user, create_message, get_messages_by_user
from chatbot import create_huggingface_response

api_router = APIRouter()


@api_router.post("/register/")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return {"message": "User registered successfully"}


@api_router.post("/login/", response_model=Token)
async def login_for_access_token(form_data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.post("/send_message/")
async def send_message(message: MessageCreate):
    try:
        ai_response = await create_huggingface_response(message.text)
        return {"user_message": message.text, "chatbot_response": ai_response}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



@api_router.get("/messages/")
async def get_messages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = get_messages_by_user(db, current_user.id)
    return [{"user_message": msg.text, "chatbot_response": msg.response} for msg in messages]


@api_router.get("/")
async def default_resp():
    return {"message": "User registered successfully"}
