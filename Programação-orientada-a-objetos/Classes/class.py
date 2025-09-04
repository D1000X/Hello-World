class refrigerante:
    def __init__(self):
        self.nome = "refrigerante"
        self.litros = 2.0
        self.preço = 10.00
    def abrir(self):
        print("abrindo o refrigerente")
    def beber(self):
        print("bebendo o refrigerente")
    def fechar(self):
        print("fechando o refrigerante")

refrigerante1 = refrigerante()
refrigerante1.abrir()
refrigerante1.beber()
refrigerante1.fechar()
refrigerante1.litros = 2.0
refrigerante1.preço = 13.00
refrigerante1.nome = "coca-cola"
print(refrigerante1.litros)
print(refrigerante1.preço)
print(refrigerante1.nome)