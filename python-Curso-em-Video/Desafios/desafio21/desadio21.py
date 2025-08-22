import pygame
# usando opygame para tocar um arquivo .mp3
pygame.init()
pygame.mixer.music.load('python-Curso-em-Video/Desafios/desafio21/vapo.mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)