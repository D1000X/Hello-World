# automação web com Selenium
from selenium import webdriver
# importando o a biblioteca time
import time
# abrir o navegador
navegador = webdriver.Chrome()
# acessar um site
navegador.get("https://www.hashtagtreinamentos.com/")
# colocar o navegador em tela chiea
navegador.maximize_window()
# Selecionar um elemento na tela.
botao_verde = navegador.find_element("Class name","botao-verde")
# clicar em um elemento
botao_verde.click()

time.sleep(10)