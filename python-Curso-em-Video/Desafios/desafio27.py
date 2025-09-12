# Programa que leia o nome completo de uma pessoa e retorne o primeiro é o ultimo nome separados.
n = input("Digite seu mome:").strip()
nome = n.split()
print(nome[0])
print(nome[len(nome)-1])