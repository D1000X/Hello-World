salario = float(input("Digite o valor do salário: "))
# Calculando o desconto de 15%
desconto = salario * 0.15
novo_salario = salario - desconto
print("O salário com 15% de desconto é R$ {:.2f}".format(novo_salario))