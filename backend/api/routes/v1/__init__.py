from fastapi import APIRouter
from .helloworld import router as hw
from .chatbot import router as chatbot

router = APIRouter()

router.include_router(hw)
router.include_router(chatbot)