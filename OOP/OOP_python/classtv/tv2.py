class Televisao:
    def __init__(self):
        #(self,canal,volume,volumeMax,volumeMin,canalMax,canalMin,ligado,desligado):
        self.canal = 1
        self.volume = 30
        self.volumeMax = 100
        self.volumeMin = 0
        self.canalMax = 100
        self.canalMin = 1
        self.ligado = False

    def ligartv(self):
        self.ligado = True

    def desligartv(self):
        self.ligado = False

    def canalUp(self):
        if not self.ligado:
            return
        if self.canal < self.canalMax:
            self.canal += 1
        else:
            return
    def canalDown(self):
        if not self.ligado:
            return
        if self.canal > self.canalMin:
            self.canal -= 1
        else:
            return

    def volumeUp(self):
        if not self.ligado:
            return
        if self.volume < self.volumeMax:
            self.volume += 10
        else:
            return
        
    def volumeDown(self):
        if not self.ligado:
            return
        if self.volume > self.canalMin:
            self.volume -= 10
        else:
            return

    def __str__(self) -> str:
        return f"Televisão --Esta Ligada ={self.ligado} - Canal:{self.canal} - Volume: {self.volume}"
    
minhatv = Televisao()
print(minhatv)

# Testando classe
# teste dos métodos ligar e desligar
tv_teste = Televisao()
print("A tv esta ligada?",tv_teste.ligado)
tv_teste.ligartv()
print("A tv esta ligada agora?",tv_teste.ligado)
tv_teste.desligartv()
print("A tv esta ligada agora ?",tv_teste.ligado)

# Teste dos métodos CanalUp é CanalDown
tv_teste.ligartv()
print("Canal atual:",tv_teste.canal)
tv_teste.canalUp()
print("Canal novo:",tv_teste.canal)
tv_teste.canalDown()
print("Novo canal:",tv_teste.canal)

# Teste dos métodos VolumeUp é VolumeDown

print("Volume atual:",tv_teste.volume)
tv_teste.volumeUp()
print("Volume novo:",tv_teste.volume)
tv_teste.volumeDown()
print("Volume new:",tv_teste.volume)