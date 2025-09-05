def For_loops():
    # Este é um loop for que imprime números de 1 a 99
    for n in range(1, 100):
        print(f"Este é um loop for que imprime {n} ")

# Este é um loop for que soma os números de 1 á 11
    for n in range(1, 11):
        soma += 1
        print(F"A soma total é {soma}")

# Este é um loop for que percorre uma lista de frutas e imprime cada fruta
    frutas = ["Maçã", "Banana", "Pera", "Uva", "Mamão"]
    for f in frutas:
        print(f)
    # Este é um loop for que percorre uma lista de némros e imprime apenas os números pares da lista.
    numeros = [2, 3, 4, 6, 7, 88, 5, 33, 45, 64]
    for m in numeros:
        if m % 2 != 0:
            continue
        print(f"{m} é um número Par")
    # Este é um loop for que percorre um dicionário e imprime suas chaves e valores
    dados = {"nome":"Jão dos venenos","idade":32,"altura":1.75,"Categoria":"Pedreiro/Maronba"}
    for c, v in dados.items():
        print(f"{c} = {v}")

def while_loops():
    # Este é um loop while que imprime números de 0 a 9
    contador = 0
    while contador < 10:
        print(f"O Contador está em {contador}")
        contador += 1

    while True:
        # Este é um loop que solicita ao usuário que digite um número par e verifica se o número é par ou impar
     numero = int(input("Digite um numero Par:"))
     if numero % 2 == 0:
        print("Você digitou um número Par!")
        break
     else:
        print("Você digitou um número Impar")

    print("Fim do programa!")


    
