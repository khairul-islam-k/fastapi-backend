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
        conn.close()

@app.get('/')
def reed_root():
    return {"Hello": "World"}

@app.get('/items')
def all_items(limit: int=5, skip: int=0, db=Depends(get_db)):
    with db.cursor() as cursor:
        sql ="""
        SELECT * FROM items
        LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (limit, skip))
        return cursor.fetchall()

@app.get("/items/{item_id}")
def read_item(item_id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
            sql ="""
            SELECT * FROM items
            WHERE id = %s
            """
            cursor.execute(sql, (item_id))
            return cursor.fetchone()

@app.post("/items")
def create_item(item: Item, db=Depends(get_db)):
    with db.cursor() as cursor:
        sql = """
        INSERT INTO items (name, description, price, tax) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (item.name, item.description, item.price, item.tax))
        db.commit()

        return {"id": cursor.lastrowid}

@app.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"id": item_id}