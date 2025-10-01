import sqlite3

name = "Juliana"
idade = 20
email = "jujudograu@gmail.com"
# Objeto de conexão com o banco de dados
banco = sqlite3.connect('Primeiro_Banco.db')
# Objeto cursor usado para executar comandos sql
cursor = banco.cursor()
# inserinado dados na tabela pessoas
#cursor.execute("INSERT INTO pessoas VALUES('"+name+"',"+str(idade)+",'"+email+"')") 

# Atualiza o campo 'name' para 'Afonso' em todas as linhas da tabela 'pessoas' onde o valor da coluna 'idade' é igual a 18
cursor.execute("UPDATE pessoas SET name = 'Afonso' WHERE idade = 18")
# Salvando as alterações no banco de dados
banco.commit()