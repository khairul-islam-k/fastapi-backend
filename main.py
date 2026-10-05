from fastapi import FastAPI, Depends
from pydantic import BaseModel
from database import get_database_connection

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    tax: float | None = None
    price: float

def get_db():
    conn = get_database_connection()
    try:
        yield conn
    finally:
        conn.close

@app.get('/')
def reed_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, name: str | None = None):
    return {"item_id": item_id, name: name}

@app.post("/items")
def create_item(item: Item):
        print(item)
        return item

@app.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
    print('id', item_id, item)
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"id": item_id}