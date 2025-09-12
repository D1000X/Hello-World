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
        self.ligartv = True

    def desligartv(self):
        self.desligartv = False

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