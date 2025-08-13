print("=== Calculadora De Média ===")
nota1 = float(input("Digite sua Primeira nota:"))
nota2 = float(input("Digite sua Segunda nota:"))
nota3 = float(input("Digite sua Terceira nota:"))
nota4 = float(input("Digite sua Quarta nota: "))
#calculo da média
soma = nota1 + nota2 + nota3 + nota4
div = soma / 4
print("Sua média do periodo é {:.2f}".format(div))
#verificação da media
print("=== Resultado ===")
if div > 6:
	print("Parabens você foi Aprovado")
elif div >= 4:
	print("Você está de recuperação")
else:
	print("Você foi reprovado")
	
