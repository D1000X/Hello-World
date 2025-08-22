from random import shuffle
# usando shuffle para embaralhar uma lista
aluno1 = input("Digite o nome do primeiro aluno:")
aluno2 = input("Digite o nome do segundo aluno:")
aluno3 = input("Digite o nome do terceiro aluno:")
aluno4 = input("Digite o nome do quarto aluno:")
lista = [aluno1, aluno2, aluno3, aluno4]
resultado = shuffle(lista)
print(f"A ordem de apresentação será {lista}")