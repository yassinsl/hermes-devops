from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

fake_items_db = []

@app.post("/items/")
def create_item(item: Item):
    fake_items_db.append(item.dict())   # save it
    return {"message": "Item created", "item": item}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0 or item_id >= len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

@app.get("/items/")
def read_all_items():
    return fake_items_db