import matplotlib.pyplot as plt

class Livro:
    def __init__(self, titulo, autor, genero, quantidade):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.quantidade = quantidade


biblioteca = []


def cadastrar_livro():
    """Função para cadastrar um novo livro."""
    print("\n--- Cadastrar Novo Livro ---")
    titulo = input("Digite o título do livro: ")
    autor = input("Digite o autor do livro: ")
    genero = input("Digite o gênero do livro: ")
    try:
        quantidade = int(input("Digite a quantidade disponível: "))
        if quantidade < 0:
            print("Quantidade não pode ser negativa.")
            return
    except ValueError:
        print("Entrada inválida. A quantidade deve ser um número inteiro.")
        return

    novo_livro = Livro(titulo, autor, genero, quantidade)
    biblioteca.append(novo_livro)
    print("Livro cadastrado com sucesso!")


def listar_livros():
    """Função para listar todos os livros."""
    if not biblioteca:
        print("\nA biblioteca está vazia.")
        return

    print("\n--- Livros Disponíveis na Biblioteca ---")
    for livro in biblioteca:
        print(
            f"Título: {livro.titulo} | Autor: {livro.autor} | Gênero: {livro.genero} | Quantidade: {livro.quantidade}")
    print("-------------------------------------------\n")


def buscar_livro_por_titulo():
    """Função para buscar um livro pelo título."""
    if not biblioteca:
        print("\nA biblioteca está vazia.")
        return

    titulo_busca = input("Digite o título do livro que deseja buscar: ")

    encontrado = False
    for livro in biblioteca:
        if livro.titulo.lower() == titulo_busca.lower():
            print("\n--- Livro Encontrado ---")
            print(
                f"Título: {livro.titulo} | Autor: {livro.autor} | Gênero: {livro.genero} | Quantidade: {livro.quantidade}")
            encontrado = True
            break

    if not encontrado:
        print("Livro não encontrado na biblioteca.")


def gerar_grafico_por_genero():
    if not biblioteca:
        print("\nA biblioteca está vazia. Não é possível gerar o gráfico.")
        return

    contagem_generos = {}
    for livro in biblioteca:
        genero = livro.genero
        contagem_generos[genero] = contagem_generos.get(genero, 0) + livro.quantidade

    generos = list(contagem_generos.keys())
    quantidades = list(contagem_generos.values())

    # Cores diferentes para cada barra
    cores = plt.cm.Paired(range(len(generos)))

    plt.figure(figsize=(12, 7))
    barras = plt.bar(generos, quantidades, color=cores)

    # Adiciona os valores no topo de cada barra
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width() / 2, altura + 0.5,
                 f'{int(altura)}', ha='center', va='bottom', fontsize=10)

    plt.title('📚 Quantidade de Livros por Gênero', fontsize=16, fontweight='bold')
    plt.xlabel('Gênero', fontsize=14)
    plt.ylabel('Quantidade de Livros', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def menu_principal():
    """Menu principal do sistema de gerenciamento da biblioteca."""
    while True:
        print("\n--- Menu da Biblioteca ---")
        print("1. Cadastrar novo livro")
        print("2. Listar todos os livros")
        print("3. Buscar livro por título")
        print("4. Gerar gráfico de livros por gênero")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cadastrar_livro()
        elif escolha == '2':
            listar_livros()
        elif escolha == '3':
            buscar_livro_por_titulo()
        elif escolha == '4':
            gerar_grafico_por_genero()
        elif escolha == '5':
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


menu_principal()
