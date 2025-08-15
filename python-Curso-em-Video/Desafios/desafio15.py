print("=== Calculadora de Aluguel de Carro ===")
dias = int(input("Por quantos dias você utilizou o carro:"))
kms =float(input("Quantos quilômetros você percorreu:"))
resdias = dias * 60
reskms = kms * 0.15
restotal = resdias + reskms
#forma mais simplis total = (dias * 60) + (kms * 0.15)
print("Você rodou por {}, é percorreu {} kms, no total seu débito é de {} reais.".format(dias,kms,restotal))