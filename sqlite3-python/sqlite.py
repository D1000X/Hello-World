import sqlite3

try:
    banco = sqlite3.connect('Primeiro_Banco.db')
    cursor = banco.cursor()

    # Executa o DELETE e verifica quantas linhas foram afetadas
    cursor.execute("DELETE FROM pessoas WHERE idade = 27")
    if cursor.rowcount > 0:
        print("Os dados foram removidos com sucesso!!!")
    else:
        print("Nenhum dado com idade 27 foi encontrado para remoção.")

    banco.commit()

except sqlite3.Error as erro:
    print("Erro ao excluir:", erro)

finally:
    banco.close()