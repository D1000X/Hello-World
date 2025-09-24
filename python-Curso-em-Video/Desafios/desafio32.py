from datetime import date
ano = int(input("Digite um ano para anlizar, digite 0 para anlizar data atual: "))

if ano == 0:
    ano = date.today().year
if ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0:
    print(f"O ano de {ano} é Bissexto.")
else:
    print(f"O ano de {ano} não e Bissexto.")