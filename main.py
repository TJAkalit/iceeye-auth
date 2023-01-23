from fastapi import FastAPI
from auth import auth

app = FastAPI()
app.include_router(auth, prefix='/auth')