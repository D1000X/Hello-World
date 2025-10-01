num = int(input("Digite um numero inteiro:"))
while True:
    print('''Escolha uma das bases para a conversão:
    [1] Converter para Binario
    [2] Converter para Octal
    [3] Converter para Hexadecimal''')
    opcao = int(input("Digite sua opção:"))

    if opcao == 1:
        binario = bin(num)[2:]
        print(f"O número {num} convertido Para Binario e {binario}")
        break
    elif opcao == 2:
        octal = oct(num)[2:]
        print(f"O número {num} convertido Para Octal e {octal}")
        break
    elif opcao == 3:
        hexadecimal = hex(num)[2:]
        print(f"O número {num} convertido Para Hexadecimal e {hexadecimal}")
        break
    else:
        print("Opção invalida, Você tem que escolher uma das três opçõis.")