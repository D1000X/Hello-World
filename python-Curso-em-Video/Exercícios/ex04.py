# Trabalhando com Blibliotecas no Python (math/sqrt).
import math
num = int(input("Digite um numero:"))
# utilizando a blibioteca math para calcular a raiz quadrada.
# math.sqrt() é a função que calcula a raiz quadrada.
raiz = math.sqrt(num)
print("A raiz de {} é {}".format(num,math.ceil(raiz)))
# math.ceil() é a função que arredonda para cima.