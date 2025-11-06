from fastapi import APIRouter, Request

router = APIRouter(prefix='/test')

@router.get('/hw')
async def hello_world(req:Request):
    return {
        'msg': 'Hello world from microservices',
        'ip': req.client.host
    }