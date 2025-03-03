import psycopg2


def connection_db():


   conn = psycopg2.connect(
       database = "activitat11",
       user="user",
       password = "pass",
       host = "localhost",
       port = "5434"
   )


   print("Connexió establerta correctament")
   return conn


