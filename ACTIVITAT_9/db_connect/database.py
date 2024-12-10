import psycopg2

# Configuració de la connexió a PostgreSQL
DATABASE_URL = "postgresql://postgres:abde@localhost:5432/practicam7"

def get_users():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    # Executo la consulta per obtenir tots els usuaris de la taula
    cursor.execute("SELECT id, name, email, age FROM users")
    users = cursor.fetchall()

    # Tanco la connexió
    cursor.close()
    connection.close()

    return users
