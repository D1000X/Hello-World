import sqlite3
# Crinado Banco de dados
# Objeto de conexão com o banco de dados
banco = sqlite3.connect('Primeiro_Banco.db')
# Objeto cursor usado para executar comandos sql
cursor = banco.cursor()
# crinado tabela
#cursor.execute("CREATE TABLE pessoas(name text,idade integer,email text)")
# inserinado dados na tabela pessoas
cursor.execute("INSERT INTO pessoas VALUES('galadriel',5000,'galadrielelfapotente@gamil.com')")
# Salvando as alterações no banco de dados
banco.commit()
# lendo dados da tabela pessoas
#cursor.execute("SELECT * FROM pessoas")
# mostrando os dados lidos no terminal
#print(cursor.fetchall())
