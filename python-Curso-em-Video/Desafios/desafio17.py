# Teorema de pitágoras forma bruta.
# cateto1 = float(input("Digite o cateto 01:"))
# cateto2 = float(input("Digite o cateto 02:"))
# hipo = (cateto1 ** 2) + (cateto2 ** 2) ** 0.5
# print("A hipotenusa é {:.3f}".format(hipo))

# Teorema de pitágoras usando a biblioteca math, sqrt.
from math import sqrt
cateto_oposto = float(input("Digite o cateto oposto:"))
cateto_adjacente = float(input("Digite oo cateto adjacente:"))
hipotenusa = sqrt(cateto_oposto ** 2 + cateto_adjacente ** 2)
print("A hipotenusa é {:.3f}".format(hipotenusa))
