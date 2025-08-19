from math import floor,trunc
num = float(input("Digite um numero:"))
comver = math.floor(num)
print("O número {} , foi arredondado para {}".format(num, comver))
# Comando floor arredonda para baixo.

# Comando trunc remove a parte decimal, sem arredondar.
import math
num = float(input("Digite um número: "))
comver = math.trunc(num)
print("O número {} foi convertido para {}".format(num, comver))
# Comando trunc remove a parte decimal, sem arredondar.
#Ambos funcionam, mas trunc apenas corta a parte decimal, enquanto floor sempre arredonda para baixo.
#Se o objetivo é só transformar em inteiro, trunc ou int() são mais indicados.