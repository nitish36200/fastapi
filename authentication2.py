'''
Authentication 
1. JWT -- Json web token
2. token-based auth (3 type-- Header, Payload, Signature)
3. Login API
'''
from fastapi import FastAPI, Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
#jwt config
SECRET_KEY = "mysecret"
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM = "HS256"  # there are many algorithm 

#paasword haashing setup
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#OauthSetup
outh2_schema = OAuth2PasswordBearer(tokenUrl="login")

#Dummy user DB
fake_user_db={
    "admin":{
        "username":"admin",
        "hashed_password": pwd_context.hash("1234")
    }
}
#HAsh Password
def hash_password(password:str):
    return pwd_context.hash(password)

#verify Password
def verify_password(plain_passwrod, hashed_password):
    return pwd_context.verify(plain_passwrod,hashed_password)

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

#Login API()
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm= Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code= 400,
            detail="Invalid Username or password "
        )
    access_token = create_token({"sub":form_data.username})
    return {
        "access_toekn": access_token,
        "token": "bearer"
    }
#token verify
def verify_token(token:str=Depends(outh2_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
           raise HTTPException(
            status_code= 401,
            detail= " Invalid token"
        )
        return username
    except jwt.JWTError:
     raise HTTPException(
        status_code=401,
        detail="Inalid Token"
    )

#protected route
@app.get("/secure")
def secure_data(user= Depends(verify_token)):
    return {
        "Message": "Secure data accessed",
        "user": user
    }  
