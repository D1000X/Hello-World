num1 = int(input("Digite um numero:"))
num2 = int(input("Digite outro numero:"))
s = num1 + num2
m = num1 * num2
d = num1 / num2
di = num1 // num2
p = num1 ** num2
#Exemplo de operadores aritméticos na prática
print("A soma é {},\n o produto é {},\n a Divisão é {:.3f}".format(s,m,d),end="  ")
print("A Divisão inteira é {},\n a Potencia é {:.3f}".format(di,p))

