import random
print("Estou pensando em um numero entre 0 e 5 .")
num = int(input("Em que numero eu estou pensando?:"))
n = random.randint(0,5)
if num == n:
    print("Parabens! Você acertou!")
else:
    print(f"Você errou! eu pensei no número {n} é não no {num}")


