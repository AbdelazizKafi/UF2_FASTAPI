from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Benvingut a la pàgina inicial"}

@app.get("/item/{item_id}")
def get_item(item_id: int):
    return {"message": f"S'ha introduït l'element amb ID: {item_id}"}

@app.get("/items/")
def get_items():
    return {"items": [
        {"id": 1, "name": "Usuari A"},
        {"id": 2, "name": "Usuari B"},
        {"id": 3, "name": "Usuari C"},
    ]}

@app.get("/user/{username}")
def get_user(username: str):
    return {"message": f"Hola, {username}, benvingut a la meva pràctica :)"}

@app.get("/calculate/")
def calculate(a: int, b: int):
    result = a + b
    return {"operation": "suma", "a": a, "b": b, "result": result}
