print("=== Calculadora de descontos ===")
# Calculadora de descontos
valor = float(input("Digite o valor do produto:"))
desconto = valor * 0.05
valor_final = valor - desconto
print("O valor final do produto ficou {} reais".format(desconto))
