import pyautogui
import time
print(pyautogui.position())
# position () esse método retorna a posição atual do mause
print(pyautogui. size())
# size() esse métudo retorna a resolução da tela

# Função de mause 
time.sleep(3) # espere 3 segundos antes de executar o clique
#pyautogui.click(x=653, y=435) # clique com o mause
pyautogui.moveTo(653,435, duration=3) # move o mause para a pisição determinada
pyautogui.click()
