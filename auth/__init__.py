from fastapi import APIRouter, HTTPException, Response, Cookie
from fastapi.responses import JSONResponse
from staff.datamodels import (
    Credentials,
    UserCreate,
)
from staff.dbmodels import User
from staff.db import Session
from staff.password import verifyPassword, hashPassword, encodeToken, decodeToken
from sqlalchemy import select, insert
import datetime

auth = APIRouter()

@auth.post('/login')
async def login(creds: Credentials):
    
    COOKIE_KEY = 'IE_AUTH'
    DOMAIN = '127.0.0.1'
    
    async with Session() as s0:
        
        query = select(User).where(User.login==creds.login)
        result = await s0.execute(query)
        dataset = [x for x in result.fetchall()]
        if dataset.__len__() ==0:
            raise HTTPException(401, 'Wrong login or password')
        if not verifyPassword(creds.password, dataset[0][0].password):
            raise HTTPException(401, 'Wrong login or password')
        
        response = JSONResponse(content={'result': 'Authorized'}, status_code=202)
        
        response.set_cookie(
            key=COOKIE_KEY,
            value=encodeToken({'user_id': dataset[0][0].id}),
            max_age=60*60*24,
            domain=DOMAIN,
            path='/auth/renew',
            httponly=True,
        )

    return response

@auth.post('/user')
async def userCreate(user: UserCreate, IE_AUTH_MAIN: str | None = Cookie(default=None)):
    
    if not IE_AUTH_MAIN:
        raise HTTPException(401)
    
    async with Session() as s0:
        data = {key: value for key, value in user}
        data['password'] = hashPassword(data['password'])
        query = insert(User).values(data).returning(User.id)
        result = await s0.execute(query)
        objId = result.fetchone()[0]
        await s0.commit()
        
    return {'userId': objId}
        
@auth.get('/renew')
async def renewToken(IE_AUTH: str | None = Cookie(default=None)):
    
    if not IE_AUTH:
        raise HTTPException(401)

    data = decodeToken(IE_AUTH)
    async with Session() as s0:
        
        query = select(User).where(User.id==data['user_id'])
        result = await s0.execute(query)
        dataset = [x for x in result]
        
        if dataset.__len__() != 1:
            raise HTTPException(401)
        
        user = dataset[0][0]
        
        metaData = {
            'id': user.id,
            'login': user.login,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'email': user.email,
            'exp': (
                datetime.datetime.now() + datetime.timedelta(seconds=30)    
            ).isoformat()
        }

        response = JSONResponse(content={'Result': 'Renewed'})
        response.set_cookie(
            'IE_AUTH_MAIN',
            value=encodeToken(metaData),
            path='/',
            httponly=True,
        )

    return response
