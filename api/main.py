from fastapi import FastAPI #type: ignore
import os

app = FastAPI()

MY_SECRET = os.environ.get("MY_SECRET", "fallback_if_not_set")

@app.get("/")
def root():
    return {"message": "Hello ji namaste"}

@app.get("/api")
def api():
    return {"message": "Hello ji namaste from api"}

@app.get("/secret_key")
def secret_key():
    return {"MY_SECRET": MY_SECRET}

