import pygame
import math 
import sys

pygame.init()

#okno

Rozliseni_okna_x = 1500
Rozliseni_okna_y = 750
okno_aplikace = pygame.display.set_mode((Rozliseni_okna_x, Rozliseni_okna_y))

#herní loop
fps_casovac = pygame.time.Clock()

while True:
    
    okno_aplikace.fill((173, 253, 255 ))

    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    #   1.level
    pygame.draw.rect(okno_aplikace, (40, 133, 16),(0, 450, 350, 300))

    pygame.display.update()
    
    fps_casovac.tick(60)   