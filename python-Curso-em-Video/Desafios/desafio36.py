valor_casa = float(input("Digite o valor da casa que voê quer comprar:"))
anos =int(input("Digite em quantos anos você vai pagar:")) 
salario = float(input("Digite o valor do seu salario:"))
prestacao = valor_casa / (anos * 12)
limete_de_prestacao = salario * 0.30
if prestacao <= limete_de_prestacao:
    print("Parabens seu emprestimo foi aprovado")
else:
    print("Seu emprestimo foi negado")