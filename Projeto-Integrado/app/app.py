pacientes = []

# Função para cadastrar um paciente


def cadastrar_paciente():
    nome = input("Nome do paciente: ")
    idade = int(input("Idade do paciente: "))
    telefone = input("Telefone do paciente: ")
    paciente = {"nome": nome, "idade": idade, "telefone": telefone}
    pacientes.append(paciente)
    print("Paciente cadastrado com sucesso!")


# Loop principal do sistema
while True:
 print("=== Sistema Clinica Vida+ ===")
 print("1. Cadastrar Paciente")
 print("2. Sair")
 opcao = input("Escolha uma opção: ")

 if opcao == "1":
    cadastrar_paciente()
 elif opcao == "2":
            break
 else:
     print("Opção inválida.")
