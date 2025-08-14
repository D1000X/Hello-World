largura = float(input("Digite a largura em metros da sua parede:"))
altura = float(input("Digite a Altura em metros da sua parede:"))
# Calculando a área total de uma parede
area = largura * altura
tinta = area / 2
print("A área total da parede é {:.2f} m2, o total de litros de tinta é de {:.2f} litros".format(area,tinta))
