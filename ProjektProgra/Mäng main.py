import pygame
import mängu_kindlad_seaded as k
import json
from vaenlased_osa import Vaenlane
from maailm import Maailm
from kahuri_osa import Kahur

pygame.init()

#Clock
clock = pygame.time.Clock()

#ekraan

ekraan = pygame.display.set_mode((k.ekraani_laius, k.ekraani_pikkus))

pygame.display.set_caption("Kvassmeister Kalja Sõda TTD")

#laeb erinevaid pilte
vaenlane_pilt = pygame.image.load("vaenlane.png").convert_alpha()
#kaart
kaart = pygame.image.load("ajutine proov.png").convert_alpha()

#kahurid
hiirekahur = pygame.image.load("kahurpeaks.png").convert_alpha()


#Gruppid

vaenlane_grupp = pygame.sprite.Group()

kahuri_grupp = pygame.sprite.Group()

#Json info
with open("ajutine.tmj") as fail:
    maailm_info = json.load(fail)
#Maailm
maailm = Maailm(maailm_info, kaart)

maailm.protsess_info()

vaenlane = Vaenlane(maailm.sihid, vaenlane_pilt)
vaenlane_grupp.add(vaenlane)

#funktsioonid
def loo_relv(hiirepos):
    hiire_koord_x = hiirepos[0] // k.ruut
    hiire_koord_y = hiirepos[1] // k.ruut
    
    hiir = (hiire_koord_y * k.veerg) + hiire_koord_x
   
    #proovi kaardil/mappil on muru id 7
    if maailm.kaardi_ruut[hiir] == 7:
        ruum_vaba = True
        for kahur in kahuri_grupp:
            if (hiire_koord_x, hiire_koord_y) == (kahur.x_koordinaat, kahur.y_koordinaat):
                ruum_vaba = False
        if ruum_vaba == True:
            ukahur = Kahur(hiirekahur, hiire_koord_x, hiire_koord_y)
            kahuri_grupp.add(ukahur)




# run-ile saab anda väärtuse False, et mängu kinni panna
run = True
#mängu loop e. mäng
while run:
    
    clock.tick(k.FPS)
    ekraan.fill("black")
    
    #joonistab kaardi
    maailm.draw(ekraan)
    
    #joonistab vaenlaste tee praegu näiteks
    pygame.draw.lines(ekraan, "black", False, maailm.sihid)
    
    #uuendame gruppe pilte (vaenlase juures asukohta)
    vaenlane_grupp.update()
        
    
    #ekraanile joonistamine
    vaenlane_grupp.draw(ekraan)
    kahuri_grupp.draw(ekraan)
    
    
    #sündmused
    for event in pygame.event.get():
        #mängu protsessi peatamine
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hiirepos = pygame.mouse.get_pos()
            #vaatab kas hiir ekraanil
            if hiirepos[0] < k.ekraani_laius and hiirepos[1] < k.ekraani_pikkus:
                loo_relv(hiirepos)
    
    
    #uuendab ekraani
    pygame.display.flip()
            
            
pygame.quit()