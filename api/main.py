from fastapi import FastAPI #type: ignore
from typing import Dict
import os

app = FastAPI()

MY_SECRET = os.environ.get("MY_SECRET", "fallback_if_not_set")

@app.get("/")
def root():
    return {"message": "Backend is working fine"}

@app.post("/login")
def api(user: Dict):
    return {"received user data": user}

@app.get("/secret_key")
def secret_key():
    return {"MY_SECRET": MY_SECRET}

