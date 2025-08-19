# Inportando função da bliblioteca math
from math import ceil
num = int(input("Digite um numero:"))
raiz = ceil(num **(1/2))
print("A raiz quadrada de {} é {}".format(num,raiz))