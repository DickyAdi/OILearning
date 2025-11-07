from fastapi import APIRouter, UploadFile
from typing import Optional

router = APIRouter()


@router.post('/chat')
async def chatbot(prompt:str, pdf_file:Optional[UploadFile]=None):
    return {
        'msg': 'Hai from chatbot endpoint'
    }