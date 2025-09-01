number = input("Digite um numero de 0 a 9999:")
new = number.zfill(4)# garantr que terá 4 digitos
print (f"A unidade de {new[-1]}")
print(f"A dezena de {new[-2]}")
print(f"A centena de {new[-3]}")
print(f"A minhar de {new[-4]}")