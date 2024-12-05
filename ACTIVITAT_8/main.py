from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    in_stock: bool

fake_db = {
    1: {"name": "Element A", "description": "Descripció A", "price": 100.0, "in_stock": True},
    2: {"name": "Element B", "description": "Descripció B", "price": 200.0, "in_stock": False},
    3: {"name": "Element C", "description": "Descripció C", "price": 300.0, "in_stock": True,}
}

@app.get("/")
def read_root():
    return {"message": "Benvingut a la pàgina inicial"}

@app.get("/item/{item_id}")
def get_item(item_id: int):

    if item_id not in fake_db:

        raise HTTPException(status_code=404, detail=f"Item amb ID {item_id} no trobat")
    return fake_db[item_id]

@app.get("/items/")
def get_items():
    return {"items": [
        {"id": 1, "name": "Usuari A", "description": "Descripció A", "preu": 100.0, "in_stock": True},
        {"id": 2, "name": "Usuari B", "description": "Descripció B", "preu": 200.0, "in_stock": False},
        {"id": 3, "name": "Usuari C", "description": "Descripció C", "preu": 300.0, "in_stock": True},
    ]}

@app.get("/user/{username}")
def get_user(username: str):
    return {"message": f"Hola, {username}, benvingut a la meva pràctica :)"}

@app.get("/calculate/")
def calculate(a: int, b: int):
    result = a + b
    return {"operation": "suma", "a": a, "b": b, "result": result}

@app.post("/item/")
def create_item(item: Item):
    fake_db[item.id] = item.dict()
    return {"message": f"Element creat: {item.name} amb ID {item.id}"}
