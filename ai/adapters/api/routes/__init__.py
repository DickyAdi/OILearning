from fastapi import APIRouter

from .helloworld import router as hw

router = APIRouter(prefix='/ai')

router.include_router(hw)