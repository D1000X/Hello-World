def conjuntos():
    conjunto = {10,20,30,40,50}
    elementos = int(input("Digite um numero é verifique se faz ou não parte do conjunto:"))

    if elementos in conjunto:
     print(f"{elementos} esta no conjunto!")
     print("Vamos removelo")
     conjunto.remove(elementos)
     print(conjunto)
    else:
     print(f"{elementos} não esta no conjunto!")
     print("Vamos adicionalo")
     conjunto.add(elementos)
     print(conjunto)
     print(conjuntos())

    
def dicionarios():
    discionario = {"ipod":2000,"ipad":4000,"Apple watch":3500,"MacBook":8000}
    # Remove o item com a chave "ipod"
    discionario.pop("ipod")
    print(discionario)
    # Adiciona um novo item com a chave ja exitente.
    # Se a chave não existir ela será criada.
    discionario["Iphone"] = 7500
    discionario["ipad"] = 4500
    print(discionario)
    # Mostra o vaLor associado a chave ex "ipad"
    print(discionario["ipad"])
    # Verifica se um item existe no dicionario
    if "MacBook" in discionario:
        print("MacBook esta no dicionario")
        print(discionario["MacBook"])
    else:
        print("MacBook não esta no dicionario")

    # Verifica se um valor existe no dicionario.
    if 3500 in discionario.values():
        print("O valor 3500 esta no dicionario")
    else:
         print("O valor 3500 não esta no dicionario")


produtos = {"ipod":2000,"ipad":4000,"Apple watch":3500,"MacBook":8000}
nome_do_produtO = input("Digite o nome do produto:")
preco_do_produto= float(input("Digite o Valor do produto:"))
nome_do_produtO = nome_do_produtO.lower()
produtos[nome_do_produtO] = preco_do_produto
novo_peco = produtos[nome_do_produtO] * 1.1
produtos[nome_do_produtO] = novo_peco
print(produtos)