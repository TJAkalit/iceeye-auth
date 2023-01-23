import bcrypt
from typing import Any
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import jwt


class SigletonMeta(type):
    
    ises = {}
    
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        
        if cls not in cls.ises:
            cls.ises[cls] = super().__call__(*args, **kwds)
        
        return cls.ises[cls]

class KeyVault(metaclass=SigletonMeta):
    
    openKey = None
    secretKey = None
    
    def __init__(self):
        
        with open('key.pem', 'rb') as file:
    
            self.secretKey = file.read()
        
        with open('key.crt', 'rb') as file:
    
            self.openKey = file.read()

    @property
    def publicKey(self)-> bytes:
        
        return self.openKey
    
    @property
    def privateKey(self)-> bytes:
        
        return self.secretKey

def hashPassword(password: str)-> bytes:
    
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

def verifyPassword(password: str, hash: str)-> bool:
    
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def encodeToken(payload: dict):
    
    return jwt.encode(
        payload=payload,
        key=KeyVault().privateKey,
        algorithm='RS256',
    )
    
def decodeToken(data: str):
    
    return jwt.decode(
        jwt=data,
        key=KeyVault().publicKey,
        algorithms=['RS256'],
        verify=True,
    )



