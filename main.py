import pygame
import math 
import sys

pygame.init()

#okno

Rozliseni_okna_x = 1500
Rozliseni_okna_y = 750
okno_aplikace = pygame.display.set_mode((Rozliseni_okna_x, Rozliseni_okna_y))

#hráč

spawn_x = 100
spawn_y = 400
hrac_x = spawn_x
hrac_y = spawn_y
velikost_hrace_x = 50
velikost_hrace_y = 50
barva_hrace = (220, 50, 23,)
vyska_skoku = -15
gravitace = 0.8
rychlost_nahoru = 0
skok = True
pokusy = 0
pokusy_celk = 0
na_zemi = False


#dash
dash = True
dashuje = False
rychlost_dashe = 0
smer = 1
max_rychlost_dashe = 30
zpomaleni_dashe = 1

#u směru 1=doprava 0=doleva

#překážky
prekazky_lvl_1 = [
    pygame.Rect(0, 450, 350, 300),      
    pygame.Rect(575, 0, 150, 500),      
    pygame.Rect(900, 300, 600, 650)     
]

#herní loop
fps_casovac = pygame.time.Clock()

hodiny = pygame.time.Clock()

while True:
    
    okno_aplikace.fill((173, 253, 255 ))

    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
   
    hrac_rect = pygame.Rect(hrac_x, hrac_y, velikost_hrace_x, velikost_hrace_y)
    na_zemi = False
    gravitace = 0.8
   
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

    #kolize
   
    #s překážkami
    for prekazaka in prekazky_lvl_1:
     if hrac_rect.colliderect(prekazaka): 
        prekryv_x = min(hrac_rect.right, prekazaka.right) - max(hrac_rect.left, prekazaka.left)
        if hrac_rect.bottom > prekazaka.top and rychlost_nahoru > 0 and prekryv_x > velikost_hrace_x/2:
            hrac_y = prekazaka.top - velikost_hrace_y 
            rychlost_nahoru = 0
            na_zemi = True
        elif not na_zemi:
            if hrac_rect.right > prekazaka.left and hrac_rect.left < prekazaka.left:
             hrac_x = prekazaka.left - velikost_hrace_x 
            if hrac_rect.left < prekazaka.right and hrac_rect.right > prekazaka.right:
             hrac_x = prekazaka.right 
    #s rohy obrazud
    if hrac_y > Rozliseni_okna_y:
        hrac_y = spawn_y
        hrac_x = spawn_x
        pokusy += 1
    if hrac_x < 0:
        hrac_x = 0
    if hrac_x + velikost_hrace_x > Rozliseni_okna_x:
        hrac_x = Rozliseni_okna_x - velikost_hrace_x
    if hrac_y < 0:
        hrac_y = 0

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
    
    #Dash

    if tlacitka[pygame.K_LSHIFT] and dash and not dashuje:
        dashuje = True
        dash = False
        rychlost_dashe = max_rychlost_dashe
    if dashuje:
        if smer == 1:
            hrac_x += rychlost_dashe
        else:
            hrac_x -= rychlost_dashe
        
        if rychlost_dashe > 0:
            rychlost_dashe -= zpomaleni_dashe
        if rychlost_dashe <= 0:
            rychlost_dashe = 0
            dashuje = False

    if hrac_y > 700:
        hrac_y = 700
        rychlost_nahoru = 0
        skok = True
    if na_zemi:
        gravitace = 0
        skok = True
    
    pygame.display.update()
    
    fps_casovac.tick(60)   