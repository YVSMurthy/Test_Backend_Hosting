from fastapi import FastAPI, Header, HTTPException #type: ignore
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware #type: ignore
import jwt #type: ignore
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError #type: ignore
from dotenv import load_dotenv #type: ignore
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

MY_SECRET = os.environ.get("MY_SECRET", "fallback_if_not_set")

@app.get("/")
def root():
    return {"message": "Backend is working fine"}

@app.get("/login")
def login(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "")
    secret = os.getenv("SUPABASE_JWT_SECRET")

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"], audience="authenticated")
        return {"user": decoded}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/secret_key")
def secret_key():
    return {"MY_SECRET": MY_SECRET}

