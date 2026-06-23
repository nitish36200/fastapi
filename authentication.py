'''
Authentication 
1. JWT -- Json web token
2. token-based auth (3 type-- Header, Payload, Signature)
3. Login API
'''
from fastapi import FastAPI, Depends, HTTPException, Header
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2Paa, OAuth2PasswordRequestForm
from passlib.context import CryptContext 

app = FastAPI()

SECRET_KEY = "mysecret"

ALGORITHM = "HS256"  # there are many algorithm 

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

#Login API(tokenGEnrate)
@app.post("/")
def login(username:str, password:str):
    if username != "admin" or password != "1234":
        raise HTTPException(
            status_code= 401, detail="Invalid username and password"
        )
    token = create_token({
        "sub":username     #sub:subject = it store username, email, userid
    })
    return {
        "Access_token":token
    }

#token verify
def verify_token(token:str = Header(None)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Invliad or expried token"
        )
    
#protected route
@app.get("/secure")
def secure_data(user= Depends(verify_token)):
    return {
        "Message": "Secure data accessed",
        "user": user
    }  
