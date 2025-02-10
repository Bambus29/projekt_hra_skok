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
pokusy = 1
pokusy_celk = 0
na_zemi = False
wall_grab = False
wall_grab_grab_padani = 0.5

#dash
dash = True
dashuje = False
rychlost_dashe = 0
smer = 1
max_rychlost_dashe = 30
zpomaleni_dashe = 1

#u směru 1=doprava 0=doleva
#level check
level_1_konec = False
#překážky
prekazky_lvl_1 = [
    pygame.Rect(0, 450, 350, 300),            
    pygame.Rect(900, 300, 600, 650),     
]
cil_obdelnik_lvl_1 = pygame.Rect(1150, 200, 10, 100)
cil_trojuhelnik_lvl_1 = pygame.Rect(1161, 200, 50, 50)

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
    wall_grab = False
    #   LEVEL 1 
    #překážky
    pygame.draw.rect(okno_aplikace, (40, 133, 16),(0, 450, 350, 300))
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
        if hrac_rect.bottom > prekazaka.top and rychlost_nahoru > 0 and prekryv_x > velikost_hrace_x/2 and not dashuje:
            hrac_y = prekazaka.top - velikost_hrace_y 
            rychlost_nahoru = 0
            na_zemi = True
            skok = True
        elif hrac_rect.top < prekazaka.bottom and rychlost_nahoru < 0:
            hrac_y = prekazaka.bottom
            rychlost_nahoru = 0
        elif not na_zemi:
           #pravá
            if hrac_rect.right > prekazaka.left and hrac_rect.left < prekazaka.left:
             hrac_x = prekazaka.left - velikost_hrace_x 
            if tlacitka[pygame.K_LCTRL] and smer == 1: 
                wall_grab = True
                hrac_x = prekazaka.left - velikost_hrace_x
                skok = True
            if tlacitka[pygame.K_LCTRL] and smer == 0: 
                wall_grab = True
                hrac_x = prekazaka.right 
                skok = True 
           #levá
            if hrac_rect.left < prekazaka.right and hrac_rect.right > prekazaka.right:
             hrac_x = prekazaka.right
            if tlacitka[pygame.K_LCTRL] and smer == 0:  
                wall_grab = True
                skok = True
                hrac_x = prekazaka.right
            if tlacitka[pygame.K_LCTRL] and smer == 1:  
                wall_grab = True
                skok = True
                hrac_x = prekazaka.left - velikost_hrace_x
    #s rohy obrazu
    if hrac_y > Rozliseni_okna_y:
        hrac_y = spawn_y
        hrac_x = spawn_x
        pokusy += 1
        dash = True
    if hrac_x < 0:
        hrac_x = 0
    if hrac_x + velikost_hrace_x > Rozliseni_okna_x:
        hrac_x = Rozliseni_okna_x - velikost_hrace_x
    if hrac_y < 0:
        hrac_y = 0
    #s cílem
    if hrac_rect.colliderect(cil_obdelnik_lvl_1) or hrac_rect.colliderect(cil_trojuhelnik_lvl_1):
        level_1_konec = True
    #ukončení levelu
    if level_1_konec:
        font = pygame.font.Font(None, 74)
        text = font.render("Level dokončen", True, (0, 0, 0))
        text_rect = text.get_rect(center=(Rozliseni_okna_x/2, Rozliseni_okna_y/2))
        
        text_pokusy = font.render(f"Počet pokusů: {pokusy}", True, (0, 0, 0))
        text_pokusy_rect = text_pokusy.get_rect(center=(Rozliseni_okna_x/2, Rozliseni_okna_y/2 + 50))
        
        okno_aplikace.blit(text, text_rect)
        okno_aplikace.blit(text_pokusy,text_pokusy_rect)
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

    if not na_zemi:
     if wall_grab:
        rychlost_nahoru = wall_grab_grab_padani 
    else:
        rychlost_nahoru += gravitace
    hrac_y += rychlost_nahoru
    
    pygame.display.update()
    
    fps_casovac.tick(60)   