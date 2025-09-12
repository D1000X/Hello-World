# Crindo uma classe para representar um carro
class Carro:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
# Métodos get e set são usados para acessar e modificar atributos de um objeto de forma controlada.
# O método get retorna o valor de um atributo (leitura).
# O método set altera o valor de um atributo (escrita).
# Isso permite aplicar regras, validações ou proteger os dados internos da classe.
 # Método get: retorna a marca do carro
    def get_marca(self):
        return self.marca
 # Método set: atualiza a marca do carro
    def set_marca(self,marca):
        self.marca = marca
# criamdo um  objeto da Classe Carro
meu_carro = Carro(marca = "Fiat",modelo ="Uno",ano = 2020)
# 
print("marca do carro:",meu_carro.get_marca())
meu_carro.set_marca(marca="chevette")
print("Nova marca:",meu_carro.get_marca())