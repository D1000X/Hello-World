r1 = float(input("Dgite o seguimento 01:"))
r2 = float(input("Digite o seguimento 02:"))
r3 = float(input("Digite o seguimento 03:"))

if r1 < r2 + r3 and r2 < r1 + r3 and r3 < r1 + r2:
    print("Pode ser um Triangulo")
else:
    print("Não pode ser um Trinagulo.")