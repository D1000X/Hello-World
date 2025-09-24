import sqlite3
# Crinado Banco de dados
banco = sqlite3.connect('Primeiro_Banco.db')

cursor = banco.cursor() 
# crinado tabela
# cursor.execute("CREATE TABLE pessoas(name texte,idade integer,email text)")
# inserinado dados
""" cursor.execute("INSERT INTO pessoas VALUES('Pedro',27,'pedroRei_delas2347@gmail.com')")
banco.commit() """
# ler dados da tabela pessoas
cursor.execute("SELECT * FROM pessoas")
print(cursor.fetchall())
 