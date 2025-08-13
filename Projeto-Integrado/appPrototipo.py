pacientes = []

def cadastrar_paciente():
    nome = input("Nome do paciente: ")
    try:
        idade = int(input("Idade do paciente: "))
    except ValueError:
        print("Idade inválida! Digite um número inteiro.")
        return
    telefone = input("Telefone do paciente: ")
    paciente = {"nome": nome, "idade": idade, "telefone": telefone}
    pacientes.append(paciente)
    print("Paciente cadastrado com sucesso!")

def ver_estatisticas():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return
    total = len(pacientes)
    media_idade = sum(p["idade"] for p in pacientes) / total
    print(f"Total de pacientes: {total}")
    print(f"Média de idade: {media_idade:.2f}")

def buscar_paciente():
    nome = input("Digite o nome do paciente para buscar: ")
    encontrados = [p for p in pacientes if p["nome"].lower() == nome.lower()]
    if encontrados:
        for p in encontrados:
            print(p)
    else:
        print("Paciente não encontrado.")

def listar_pacientes():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return
    for p in pacientes:
        print(p)

while True:
    print("\n=== Sistema Clinica Vida+ ===")
    print("1. Cadastrar Paciente")
    print("2. Ver Estatísticas")
    print("3. Buscar Paciente")
    print("4. Listar Todos os Pacientes")
    print("5. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_paciente()
    elif opcao == "2":
        ver_estatisticas()
    elif opcao == "3":
        buscar_paciente()
    elif opcao == "4":
        listar_pacientes()
    elif opcao == "5":
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")