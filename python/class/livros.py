class livros:
 def __init__(self,titulo,autor,genero,quantidade,):
    self.titulo = titulo
    self.autor = autor
    self.genero = genero
    self.quantidade = quantidade

biblioteca = []
def cadastrar_livro():
    titulo = input("Digite o titulo do livro:")
    autor = input("Digite o nome do autor:")
    genero = input("Digite o gênero do livro:")
    quantidade = int(input("Digite a quantidade:"))

new_livro = livros(titulo,autor,genero,quantidade)
biblioteca.append(new_livro)
print("LIvros cadastrado com sucesso!")

def listar_livros():
   if not biblioteca:
      print("A biblioteca está vazia.")
      return
   print("\n--- Livros Disponíveis na Biblioteca ---")
for livro in biblioteca:
        print(f"Título: {livros.titulo}, Autor: {livros.autor}, Gênero: {livros.genero}, Quantidade: {livros.quantidade}")
print("-------------------------------------------\n")
# Função para buscar um livro pelo título
def buscar_livro_por_titulo():
    titulo_busca = input("Digite o título do livro que deseja buscar: ")
    
    # Percorre a lista de livros para encontrar a correspondência
    encontrado = False
    for livros in biblioteca:
        if livros.titulo.lower() == titulo_busca.lower():
            print("\n--- Livro Encontrado ---")
            print(f"Título: {livros.titulo}, Autor: {livros.autor}, Gênero: {livros.genero}, Quantidade: {livros.quantidade}")
            print("-------------------------\n")
            encontrado = True
            break
    
    if not encontrado:
        print("Livro não encontrado na biblioteca.")
