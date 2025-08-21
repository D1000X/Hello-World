# Crindo uma classe para representar um carro
class Carro:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano


    def get_marca(self):
        return self.marca
    def set_marca(self,marca):
        self.marca = marca
# criamdo um  objeto da Classe Carro
meu_carro = Carro("Fiat", "Uno", 2020)
print(f"Marca:{meu_carro.marca},Modelo:{meu_carro.modelo},Ano:{meu_carro.ano}")
# usando os metodos get e set para acessar e modificar o atributo marca>
meu_carro.set_marca(marca ="Chevette")
print(f"Nova Marca:",meu_carro.get_marca())