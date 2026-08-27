from fastapi import FastAPI
from typing import Dict 

app = FastAPI()

@app.get("/health")
def health()-> Dict:
    return {"status" : "ok"}