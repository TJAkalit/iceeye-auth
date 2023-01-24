from fastapi import FastAPI, Request
from auth import auth

app = FastAPI()
app.include_router(auth, prefix='/auth')


@app.middleware('http')
async def secureUrls(request: Request, call_next):
    
    response = await call_next(request)
    return response