import psycopg2


def connection_db():


   conn = psycopg2.connect(
       database = "penjat",
       user="user",
       password = "pass",
       host = "localhost",
       port = "5433"
   )


   print("Connexió establerta correctament")
   return conn


