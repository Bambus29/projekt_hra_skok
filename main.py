import pygame
import math 
import sys

pygame.init()

#okno

Rozliseni_okna_x = 1500
Rozliseni_okna_y = 750
okno_aplikace = pygame.display.set_mode((Rozliseni_okna_x, Rozliseni_okna_y))

#hráč

hrac_x = 100
hrac_y = 400
velikost_hrace_x = 50
velikost_hrace_y = 50
barva_hrace = (220, 50, 23,)
vyska_skoku = -15
gravitace = 0.8
rychlost_nahoru = 0
skok = True
dash = True
smer = 1
dalka_dashe = 60
#u směru 1=doprava 0=doleva

#herní loop
fps_casovac = pygame.time.Clock()

while True:
    
    okno_aplikace.fill((173, 253, 255 ))

    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    #   LEVEL 1 
    #překážky
    pygame.draw.rect(okno_aplikace, (40, 133, 16),(0, 450, 350, 300))
    pygame.draw.rect(okno_aplikace, (40, 133, 16),(575, 0, 150, 500))
    pygame.draw.rect(okno_aplikace, (40, 133, 16),(900, 300, 600, 650))

    #cíl
    pygame.draw.rect(okno_aplikace, (0, 0, 0,),(1150, 200, 10, 100))
    pygame.draw.polygon(okno_aplikace, (255, 175, 60),[(1161, 200),(1161, 250),(1211, 225)])


    #hráč
    pygame.draw.rect(okno_aplikace, barva_hrace, (hrac_x, hrac_y, velikost_hrace_x, velikost_hrace_y))

    #ovládání
    tlacitka = pygame.key.get_pressed()

    if tlacitka[pygame.K_d]:
        hrac_x += 5
        smer = 1

    if tlacitka[pygame.K_a]:
        hrac_x -= 5
        smer = 0

    if tlacitka[pygame.K_SPACE] and skok:
        rychlost_nahoru = vyska_skoku
        skok = False
    
    rychlost_nahoru += gravitace
    hrac_y += rychlost_nahoru
    
    if tlacitka[pygame.K_LSHIFT] and dash:
        if smer == 1:
            hrac_x += dalka_dashe
        else: 
            hrac_x -= dalka_dashe
        dash = False
    

    if hrac_y > 700:
        hrac_y = 700
        rychlost_nahoru = 0
        skok = True
        dash = True
    pygame.display.update()
    
    fps_casovac.tick(60)   