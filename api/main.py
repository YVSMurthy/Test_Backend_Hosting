from fastapi import FastAPI, Header, HTTPException, Depends #type: ignore
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware #type: ignore
import jwt #type: ignore
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError #type: ignore
from sqlalchemy.orm import Session #type: ignore
from dotenv import load_dotenv #type: ignore
load_dotenv()

from database.database import SessionLocal
from database import crud

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def booleanFilter(feature_list):
    allFeatures = crud.get_all_features(db=SessionLocal())
    filtered_features = []
    for feature in allFeatures:
        if feature.feature_name in feature_list:
            filtered_features.append({
                "feature_name": feature.feature_name,
                "is_enabled": True
            })
        else:
            filtered_features.append({
                "feature_name": feature.feature_name,
                "is_enabled": False
            })
    return filtered_features

@app.get("/")
def root():
    return {"message": "Backend is working fine"}

@app.get("/get-user-role")
def login(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "")
    secret = os.getenv("SUPABASE_JWT_SECRET")

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"], audience="authenticated")
        print(decoded['sub'])
        user_role = crud.find_user_roles(db=db, user_id=decoded['sub'])

        if not user_role:
            user = crud.add_default_user_role(db=db, user_id=decoded['sub'])
            user_role = crud.find_user_roles(db=db, user_id=decoded['sub'])
            
        feature_list = [f.feature_name for f in crud.find_features_by_role(db=db, role_id=user_role[0].role_id)]

        
        print(feature_list)
        feature_list = booleanFilter(feature_list)

        return {"detail": "ok", "body":{"user": decoded['sub'], "role": user_role[0].role_type, "tier": user_role[0].tier, "features": feature_list}}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/secret_key")
def secret_key():
    return {"MY_SECRET": MY_SECRET}

