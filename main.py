import pygame
import math 
import sys

pygame.init()

#okno

Rozliseni_okna_x = 1500
Rozliseni_okna_y = 750
okno_aplikace = pygame.display.set_mode((Rozliseni_okna_x, Rozliseni_okna_y))


#hráč

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

#Textury

hrac_doprava = pygame.image.load("hrac_doprava.png")
hrac_doleva = pygame.image.load("hrac_doleva.png")

hrac_doprava = pygame.transform.scale(hrac_doprava, (velikost_hrace_x, velikost_hrace_y))
hrac_doleva = pygame.transform.scale(hrac_doleva, (velikost_hrace_x, velikost_hrace_y))

aktualni_hrac = hrac_doprava

mrak = pygame.image.load("mrak.png")

#dash
dash = True
dashuje = False
rychlost_dashe = 0
smer = 1
max_rychlost_dashe = 20
zpomaleni_dashe = 1

#u směru 1=doprava 0=doleva

#level check
level = 1
level_konec = False
hra_konec = False
#překážky, cíle, spawny
prekazky ={
    1: [ 
        pygame.Rect(0, 450, 350, 300),            
        pygame.Rect(900, 300, 600, 650)
    ,],
    
   2: [  
        pygame.Rect(0, 300, 300, 450),
        pygame.Rect(500, 0, 200, 350),
        pygame.Rect(500, 500, 200, 350),
        pygame.Rect(1100, 300, 100, 450),
        pygame.Rect(1300, 700, 200, 50),
    ],
    3:[
        pygame.Rect(0, 700, 200, 50),
        pygame.Rect(300, 500, 150, 100),
        pygame.Rect(700, 400, 200, 200),
        pygame.Rect(1345, 300, 75, 75)
        
    ],
    4: [
        pygame.Rect(50, 300, 75, 75),
        pygame.Rect(450, 700, 200, 50),
        pygame.Rect(750, 700, 200, 50),
        pygame.Rect(500, 300, 150, 50),
        pygame.Rect(1000, 500, 200, 50),
        pygame.Rect(1000, 300, 200, 50),
        pygame.Rect(150, 700, 200, 50),
        pygame.Rect(350, 0, 100, 400)

    ] 
    }
        
cile ={
   1: { 
        'obdelnik' : pygame.Rect(1150, 200, 10, 100),
        'trojuhelnik' : pygame.Rect(1161, 200, 50, 50)
    },

    2: {
        'obdelnik': pygame.Rect(1395, 600, 10, 100),
        'trojuhelnik': pygame.Rect(1406, 600, 50, 50)
    },

    3:{
        'obdelnik': pygame.Rect(1370, 200, 10, 100),
        'trojuhelnik': pygame.Rect(1381, 200, 50, 50)
    },
    4: {
        'obdelnik': pygame.Rect(540, 200, 10, 100),
        'trojuhelnik': pygame.Rect(551, 200, 50, 50)
    }
    }
spawn_pointy = {
    1: {"x": 100, "y": 400},  
    2: {"x": 50, "y": 200},
    3: {"x": 100, "y": 650},
    4: {"x": 65, "y": 300}  
}

spawn_x = spawn_pointy[1]["x"]  # Výchozí spawn point pro začátek hry
spawn_y = spawn_pointy[1]["y"]
hrac_x = spawn_x
hrac_y = spawn_y

#herní loop
fps_casovac = pygame.time.Clock()

hodiny = pygame.time.Clock()
#Vykreslení levelu
def vykresli_level(level):
    for prekazaka in prekazky[level]:
        mrak_scaled = pygame.transform.scale(mrak, (prekazaka.width, prekazaka.height))
        okno_aplikace.blit(mrak_scaled, (prekazaka.x, prekazaka.y))
    
    pygame.draw.rect(okno_aplikace, (0, 0, 0), cile[level]['obdelnik'])
    cil_troj = cile[level]['trojuhelnik']
    pygame.draw.polygon(okno_aplikace, (255, 175, 60),
        [(cil_troj.x, cil_troj.y),
         (cil_troj.x, cil_troj.y + 50),
         (cil_troj.x + 50, cil_troj.y + 25)])

while True:
    
    okno_aplikace.fill((173, 253, 255 ))

    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_ESCAPE:
                level = 1
                pokusy = 1
                hrac_x = spawn_pointy[1]["x"]
                hrac_y = spawn_pointy[1]["y"]
                dash = True
            if udalost.key == pygame.K_r:
                hrac_x = spawn_pointy[level]["x"]
                hrac_y = spawn_pointy[level]["y"]
                pokusy += 1
                dash = True
    
    # Textura hráče změna
    hrac_rect = pygame.Rect(hrac_x, hrac_y, velikost_hrace_x, velikost_hrace_y)

    if smer == 1:
        aktualni_hrac = hrac_doprava
    else:
        aktualni_hrac = hrac_doleva
    okno_aplikace.blit(aktualni_hrac, (hrac_x, hrac_y))
    
    
    na_zemi = False
    gravitace = 0.8
    wall_grab = False
    #LEVEL
    
    vykresli_level(level)
    
    #kolize
   
    #s překážkami
    for prekazaka in prekazky[level]:
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
            #wall bug fix
            if hrac_y < prekazaka.y and wall_grab == True:
                hrac_y = prekazaka.y
    #s rohy obrazu
    if hrac_y > Rozliseni_okna_y:
        hrac_x = spawn_pointy[level]["x"]
        hrac_y = spawn_pointy[level]["y"]
        pokusy += 1
        dash = True
        
    if hrac_x < 0:
        hrac_x = 0
    if hrac_x + velikost_hrace_x > Rozliseni_okna_x:
        hrac_x = Rozliseni_okna_x - velikost_hrace_x
    
    #s cílem
    if (hrac_rect.colliderect(cile[level]['obdelnik']) or 
        hrac_rect.colliderect(cile[level]['trojuhelnik'])):
        level_completed = True
        dash = True
        if level < len(prekazky):
            level += 1
            hrac_x = spawn_pointy[level]["x"] 
            hrac_y = spawn_pointy[level]["y"]
            level_completed = False
        else: 
            hra_konec = True
            
            pokusy_celk = pokusy
            
            if pokusy_celk <= 1:
                hvezdicky = 5
            elif pokusy_celk <= 10:
                hvezdicky = 4
            elif pokusy_celk <= 25:
                hvezdicky = 3
            elif pokusy_celk <= 50:
                hvezdicky = 2
            else:
                hvezdicky = 1
            
            pygame.draw.rect(okno_aplikace, (0, 0, 0,), (0,0, Rozliseni_okna_x, Rozliseni_okna_y) )
            font = pygame.font.Font(None, 74)
            text = font.render("Hra dokončena!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(Rozliseni_okna_x/2, Rozliseni_okna_y/2 - 50))
            okno_aplikace.blit(text, text_rect)
        
            font_pokusy = pygame.font.Font(None, 48)
            text_pokusy = font_pokusy.render(f"Počet pokusů: {pokusy_celk}", True, (255, 255, 255))
            text_pokusy_rect = text_pokusy.get_rect(center=(Rozliseni_okna_x/2, Rozliseni_okna_y/2 + 20))
            okno_aplikace.blit(text_pokusy, text_pokusy_rect)
            
            hvezdicka_rozmer = 80  
            mezera = 20
            celkova_sirka = hvezdicky * hvezdicka_rozmer + (hvezdicky - 1) * mezera
            start_x = (Rozliseni_okna_x - celkova_sirka) / 2
            
            for i in range(hvezdicky):
                x_pozice = start_x + i * (hvezdicka_rozmer + mezera)
                stred_x = x_pozice + hvezdicka_rozmer/2
                stred_y = Rozliseni_okna_y/2 + 100
                
                body_hvezdicky = []
                for j in range(5):
                    vnejsi_uhel = math.pi/2 + j * 2*math.pi/5
                    vnejsi_x = stred_x + hvezdicka_rozmer/2 * math.cos(vnejsi_uhel)
                    vnejsi_y = stred_y - hvezdicka_rozmer/2 * math.sin(vnejsi_uhel)
                    body_hvezdicky.append((vnejsi_x, vnejsi_y))
                    
                    vnitrni_uhel = vnejsi_uhel + math.pi/5
                    vnitrni_x = stred_x + hvezdicka_rozmer/5 * math.cos(vnitrni_uhel)
                    vnitrni_y = stred_y - hvezdicka_rozmer/5 * math.sin(vnitrni_uhel)
                    body_hvezdicky.append((vnitrni_x, vnitrni_y))
                
                pygame.draw.polygon(okno_aplikace, (255, 215, 0), body_hvezdicky)
    
    #ovládání
    tlacitka = pygame.key.get_pressed()

    if tlacitka[pygame.K_d] or tlacitka[pygame.K_RIGHT]:
        hrac_x += 7
        smer = 1

    if tlacitka[pygame.K_a] or tlacitka[pygame.K_LEFT]:
        hrac_x -= 7
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