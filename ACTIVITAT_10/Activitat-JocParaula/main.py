from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import read_db
import options_sch



app = FastAPI()

# Endpoint per comprobar el funcionament
@app.get("/")
async def root():
    return {"message": "Benvingut a fastapi"}

# Endpoint per obtenir les diferents temàtiques
@app.get("/penjat/tematica/opcions", response_model=List[dict])
async def get_options():
    return options_sch.options_schema(read_db.read_db())


# Endpoint per obtenir una paraula aleatoria d'una temàtica
@app.get("/penjat/tematica/{option}", response_model=List[dict])
async def get_word(option: str):
    word = options_sch.options_schema(read_db.read_word_db(option))
    return word

