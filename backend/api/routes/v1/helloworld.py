from fastapi import APIRouter, Request

router = APIRouter(prefix='/test')

@router.get('/hw')
async def hello(req:Request):
    return {
        'msg': 'Hello world from microservice',
        'ip': req.client.host
    }