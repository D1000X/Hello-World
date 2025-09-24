velocidade = float(input("Qual a velocdade atual do carro?"))
if velocidade <= 80:
    print("Tenha um bom dia! Dirija com segurança!")
else:
    multa = (velocidade - 80) * 7
    print(f"Multado!Você esta acima do limite de velocidadade que é 80 km!")
    print(f"Sua multa e de {multa} reais!")