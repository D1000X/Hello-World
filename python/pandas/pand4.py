import pandas as pd
# 01 metodo datafreme vazio 
#datafreme = pd.DataFrame()

# 02 metodo Criando um datafreme a partir de um dicionario
def dicionario():
        vendas = {'data':['15/02/2021','16/02/2021'],
        'valor': [500,300],
        'produto':['feijão','arroz'],
        'quantidade':[50,70]
        }
        vendas_df = pd.DataFrame(vendas)

        print(vendas_df)

# 03 metodo importando aquivos de uma base de dados
vendas_df = pd.read_excel("Vendas - Dez.xlsx")
print(vendas_df)
