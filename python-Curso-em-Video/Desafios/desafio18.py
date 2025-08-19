import math
# Calculando seno é conseno tangente com a biblioteca math(sin,cos,tan)
angulo = float(input("Digite o ângulo que voçê deseja:"))
seno = math.sin(math.radians(angulo))
print ("O ângulo {} tem seno {:.2f}".format(angulo,seno))
coseno = math.cos(math.radians(angulo))
print("O ângulo {} tem coseno {:.2f}".format(angulo,coseno))
tangente = math.tan(math.radians(angulo))
print("O ângulo {} tem tangente {:.2f}".format(angulo,tangente))
