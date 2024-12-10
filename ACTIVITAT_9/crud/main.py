from fastapi import FastAPI
from typing import List
from schemas import users_sch
from db_connect import database
import schemas.users_sch as users_sch 
# Importo la funció per recuperar els usuaris de la base de dades
from db_connect.database import get_users 

app = FastAPI()

@app.get("/users/", response_model=List[dict])
async def read_users():
   # Obtinc els usuaris de la base de dades
    users = get_users()  
    return users_sch.users_schema(users)
