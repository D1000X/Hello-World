distancia = float(input("Digite a distancia da sua viagem:"))
if distancia <= 20:
    cal01 = distancia * 0.50
    print(f"O valor da sua viagem é de {cal01}R$")
else:
    cal02 = distancia * 0.45
    print(f"O valor da sua viagem é de {cal02}R$")