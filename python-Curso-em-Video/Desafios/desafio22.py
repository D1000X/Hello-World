name = input("Digite seu nome completo:")
print(f"Seu nome em maiusculo:{name.upper()}")
print(f"Seu nome em menusculo:{name.lower()}")
print(f"Seu nome tem {len(name.replace("  ",""))} letras")
pname = name.split()[0]
print(f"Seu Primeiro nome tem {len(pname)} letras")
