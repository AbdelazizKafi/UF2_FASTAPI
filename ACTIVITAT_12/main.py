from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import psycopg2

# Connexió a la base de dades
def connection_db():
    return psycopg2.connect(
        database="activitat11",
        user="user",
        password="pass",
        host="localhost",
        port="5434"
    )

app = FastAPI()

class RegistreJoc(BaseModel):
    usuari_id: int
    paraula_id: int
    intents_fallits: int = 0
    estat: str
    
class Usuari(BaseModel):
    nom: str
    email: str
    contrasenya: str

class Paraula(BaseModel):
    paraula: str

class PantallaPrincipal(BaseModel):
    total_usuaris: int
    total_partides: int
    partides_guanyades: int
    partides_perdudes: int

# Enpoint per a la taula registre_joc
@app.post("/registre_joc/")
async def create_registre_joc(registre: RegistreJoc):
    conn = connection_db()
    cursor = conn.cursor()
    query = """
    INSERT INTO registre_joc (usuari_id, paraula_id, intents_fallits, estat) 
    VALUES (%s, %s, %s, %s) RETURNING id;
    """
    cursor.execute(query, (registre.usuari_id, registre.paraula_id, registre.intents_fallits, registre.estat))
    registre_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Registre creat correctament", "id": registre_id}

@app.get("/registre_joc/", response_model=List[RegistreJoc])
async def get_all_registre_joc():
    conn = connection_db()
    cursor = conn.cursor()
    query = "SELECT usuari_id, paraula_id, intents_fallits, estat FROM registre_joc;"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"usuari_id": row[0], "paraula_id": row[1], "intents_fallits": row[2], "estat": row[3]} for row in result]

@app.get("/registre_joc/{registre_id}")
async def get_registre_joc(registre_id: int):
    conn = connection_db()
    cursor = conn.cursor()
    query = "SELECT usuari_id, paraula_id, intents_fallits, estat FROM registre_joc WHERE id = %s;"
    cursor.execute(query, (registre_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"usuari_id": row[0], "paraula_id": row[1], "intents_fallits": row[2], "estat": row[3]}
    raise HTTPException(status_code=404, detail="Registre no trobat")

@app.put("/registre_joc/{registre_id}")
async def update_registre_joc(registre_id: int, registre: RegistreJoc):
    conn = connection_db()
    cursor = conn.cursor()
    query = """
    UPDATE registre_joc SET usuari_id=%s, paraula_id=%s, intents_fallits=%s, estat=%s 
    WHERE id=%s RETURNING id;
    """
    cursor.execute(query, (registre.usuari_id, registre.paraula_id, registre.intents_fallits, registre.estat, registre_id))
    updated_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if updated_id:
        return {"message": "Registre actualitzat correctament"}
    raise HTTPException(status_code=404, detail="Registre no trobat")

@app.delete("/registre_joc/{registre_id}")
async def delete_registre_joc(registre_id: int):
    conn = connection_db()
    cursor = conn.cursor()
    query = "DELETE FROM registre_joc WHERE id = %s RETURNING id;"
    cursor.execute(query, (registre_id,))
    deleted_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if deleted_id:
        return {"message": "Registre eliminat correctament"}
    raise HTTPException(status_code=404, detail="Registre no trobat")

# Enpoint per a la taula usuaris
@app.post("/usuaris/", response_model=dict)
async def crear_usuari(usuari: Usuari):
    """Crea un nou usuari"""
    try:
        conn = connection_db()
        cursor = conn.cursor()
        query = """
        INSERT INTO usuaris (nom, email, contrasenya) VALUES (%s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (usuari.nom, usuari.email, usuari.contrasenya))
        usuari_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuari creat correctament", "id": usuari_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuaris/", response_model=List[dict])
async def obtenir_usuaris():
    """Retorna tots els usuaris"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuaris;")
    usuaris = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": u[0], "nom": u[1], "email": u[2]} for u in usuaris]

@app.get("/usuaris/{usuari_id}", response_model=dict)
async def obtenir_usuari(usuari_id: int):
    """Retorna un usuari per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuaris WHERE id = %s;", (usuari_id,))
    usuari = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuari:
        raise HTTPException(status_code=404, detail="Usuari no trobat")
    return {"id": usuari[0], "nom": usuari[1], "email": usuari[2]}

@app.put("/usuaris/{usuari_id}")
async def actualitzar_usuari(usuari_id: int, usuari: Usuari):
    """Actualitza un usuari per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuaris SET nom=%s, email=%s, contrasenya=%s WHERE id=%s;",
        (usuari.nom, usuari.email, usuari.contrasenya, usuari_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Usuari actualitzat correctament"}

@app.delete("/usuaris/{usuari_id}")
async def eliminar_usuari(usuari_id: int):
    """Elimina un usuari per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuaris WHERE id=%s;", (usuari_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Usuari eliminat correctament"}


# Enpoint per a la taula paraules
@app.post("/paraules/", response_model=dict)
async def crear_paraula(paraula: Paraula):
    """Crea una nova paraula"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paraules (paraula) VALUES (%s) RETURNING id;", (paraula.paraula,))
    paraula_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Paraula creada correctament", "id": paraula_id}

@app.get("/paraules/", response_model=List[dict])
async def obtenir_paraules():
    """Retorna totes les paraules"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paraules;")
    paraules = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": p[0], "paraula": p[1]} for p in paraules]

@app.get("/paraules/{paraula_id}", response_model=dict)
async def obtenir_paraula(paraula_id: int):
    """Retorna una paraula per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paraules WHERE id = %s;", (paraula_id,))
    paraula = cursor.fetchone()
    cursor.close()
    conn.close()
    if not paraula:
        raise HTTPException(status_code=404, detail="Paraula no trobada")
    return {"id": paraula[0], "paraula": paraula[1]}

@app.put("/paraules/{paraula_id}")
async def actualitzar_paraula(paraula_id: int, paraula: Paraula):
    """Actualitza una paraula per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE paraules SET paraula=%s WHERE id=%s;", (paraula.paraula, paraula_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Paraula actualitzada correctament"}

@app.delete("/paraules/{paraula_id}")
async def eliminar_paraula(paraula_id: int):
    """Elimina una paraula per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM paraules WHERE id=%s;", (paraula_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Paraula eliminada correctament"}

# Enpoint per a la taula pantalla_principal
@app.post("/pantalla_principal/")
async def crear_pantalla_principal(pantalla: PantallaPrincipal):
    """Crea un nou registre de pantalla principal"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pantalla_principal (total_usuaris, total_partides, partides_guanyades, partides_perdudes)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (pantalla.total_usuaris, pantalla.total_partides, pantalla.partides_guanyades, pantalla.partides_perdudes))
    
    id_nou = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Pantalla principal creada correctament", "id": id_nou}

@app.get("/pantalla_principal/{id}", response_model=dict)
async def obtenir_pantalla_principal(id: int):
    """Retorna les estadístiques d'una pantalla principal per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pantalla_principal WHERE id=%s;", (id,))
    pantalla = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not pantalla:
        raise HTTPException(status_code=404, detail="No s'ha trobat la pantalla principal")
    
    return {
        "id": pantalla[0],
        "total_usuaris": pantalla[1],
        "total_partides": pantalla[2],
        "partides_guanyades": pantalla[3],
        "partides_perdudes": pantalla[4]
    }

@app.put("/pantalla_principal/{id}")
async def actualitzar_pantalla_principal(id: int, pantalla: PantallaPrincipal):
    """Actualitza les estadístiques d'una pantalla principal per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pantalla_principal 
        SET total_usuaris=%s, total_partides=%s, partides_guanyades=%s, partides_perdudes=%s 
        WHERE id=%s;
    """, (pantalla.total_usuaris, pantalla.total_partides, pantalla.partides_guanyades, pantalla.partides_perdudes, id))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pantalla principal no trobada")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Pantalla principal actualitzada correctament"}

@app.delete("/pantalla_principal/{id}")
async def eliminar_pantalla_principal(id: int):
    """Elimina un registre de pantalla principal per ID"""
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pantalla_principal WHERE id=%s;", (id,))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pantalla principal no trobada")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Pantalla principal eliminada correctament"}