import pandas as pd
import os
lista_de_vendas = os.listdir("Pandas\Vendas-20251005T192137Z-1-001.zip\Vendas")
print(lista_de_vendas)
for aquivo in lista_de_vendas:
    if "vendas" in aquivo:
        tabela_vendas = pd.read_csv(f"Pandas\Vendas-20251005T192137Z-1-001\Vendas\{aquivo}")
        print(tabela_vendas)
        print(tabela_vendas.info())
        print(tabela_vendas["valor final"].sum())
        print("Aquivo lido com sucesso!")
