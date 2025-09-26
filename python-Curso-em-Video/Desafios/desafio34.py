salario = float(input("Digite o seu salário:"))

if salario > 1250:
    result = salario + (salario * 0.10)
    print(f"Parabens Você ganhou um aumento de 10% no seu salário, seu novo salario agora é {result}")
elif salario <= 1250:
    result1 =salario + (salario * 0.15)
    print(f"Parabens Você ganhou um aumento de 15% no seu salário, seu novo salario agora é {result1}")
