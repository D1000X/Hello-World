from random import choice
# usando choice para escolher um item aleatório de uma lista
n1 = input("Digite o nome do aluno:")
n2 = input("Digite o nome do segundo aluno:")
n3 = input("Digite o nome do terceiro aluno:")
n4 = input("Digite o nome do quarto aluno:")
lista = [n1,n2,n3,n4]
resultado = choice(lista)
print(f"O aluno(a) escolhido foi {resultado}")