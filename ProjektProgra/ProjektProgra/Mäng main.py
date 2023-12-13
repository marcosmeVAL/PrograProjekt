import pygame
import mängu_kindlad_seaded as k
import json
from vaenlased_osa import Vaenlane
from maailm import Maailm
from kahuri_osa import Kahur
from nupud import Nupp

pygame.init()

#Clock
clock = pygame.time.Clock()

#ekraan

ekraan = pygame.display.set_mode((k.ekraani_laius + k.kõrval_paneel, k.ekraani_pikkus))

pygame.display.set_caption("Kvassmeister Kalja Sõda TTD")

#mängu variables
kahur_paigaldus = False 
selected_kahur = None


#laeb erinevaid pilte
#vaenlased
vaenlane_pilt = pygame.image.load("pildid/vaenlane.png").convert_alpha()
#kaart
kaart = pygame.image.load("ajutine proov.png").convert_alpha()

#kahurid
kahuri_sheetid = []
for i in range(1, k.kahur_levels + 1):
    kahuri_sheet = pygame.image.load(f"pildid/turret_{i}.png").convert_alpha()
    kahuri_sheetid.append(kahuri_sheet)
    
#hiirekahur
hiirekahur = pygame.image.load("pildid/cursor_turret.png").convert_alpha()

#nupud mängu akna kõrval
kahuri_ostmisnupp = pygame.image.load("pildid/nupkah.png").convert_alpha()
cancel_pilt = pygame.image.load("pildid/cancel.png").convert_alpha()
upg_kahur_pilt = pygame.image.load("pildid/upgrade_turret.png").convert_alpha()


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
#loo nupp
kahuri_nupp = Nupp(k.ekraani_laius + 30, 120, kahuri_ostmisnupp, True)
cancel_nupp = Nupp(k.ekraani_laius + 50, 180, cancel_pilt, True)
upg_nupp = Nupp(k.ekraani_laius + 5, 180, upg_kahur_pilt, True)


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
            ukahur = Kahur(kahuri_sheetid, hiire_koord_x, hiire_koord_y)
            kahuri_grupp.add(ukahur)
            
def clear_select():
    for kahur in kahuri_grupp:
        kahur.selected = False
        
def select_kahur(hiirepos):
    hiire_koord_x = hiirepos[0] // k.ruut
    hiire_koord_y = hiirepos[1] // k.ruut
    for kahur in kahuri_grupp:
        if (hiire_koord_x, hiire_koord_y) == (kahur.x_koordinaat, kahur.y_koordinaat):
            return kahur

# run-ile saab anda väärtuse False, et mängu kinni panna
run = True
#mängu loop e. mäng
while run:
    
    clock.tick(k.FPS)
    ekraan.fill("white")
    #UPDATID
    #uuendame gruppe pilte (vaenlase juures asukohta)
    vaenlane_grupp.update()
    kahuri_grupp.update(vaenlane_grupp)
    #
    if selected_kahur:
        selected_kahur.selected = True 
    
    
    #JOONESTAMISED
    #joonistab kaardi
    maailm.draw(ekraan)
    
    #joonistab vaenlaste tee praegu näiteks
    pygame.draw.lines(ekraan, "black", False, maailm.sihid)
    
    
    #ekraanile joonistamine
    vaenlane_grupp.draw(ekraan)
    for kahur in kahuri_grupp:
        kahur.draw(ekraan)
    
    #ekraani kõrval paneel
    #nupu joonistamine
    if kahuri_nupp.draw(ekraan):
        kahur_paigaldus = True 
    #kui kahurit pannakse alles ss näitab
    #cancel nupp
    if kahur_paigaldus == True:
        #näite kahurrit hiirel
        cursor_rect = hiirekahur.get_rect()
        curser_pos = pygame.mouse.get_pos()
        cursor_rect.center = curser_pos
        
        if curser_pos[0] <= k.ekraani_laius:
            ekraan.blit(hiirekahur, cursor_rect)
            
        if cancel_nupp.draw(ekraan):
            kahur_paigaldus = False 
    #upgrade nupp
    if selected_kahur:
        if selected_kahur.upg_level < k.kahur_levels:
            if upg_nupp.draw(ekraan):
                selected_kahur.upgrade()
    
    #sündmused
    for event in pygame.event.get():
        #mängu protsessi peatamine
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hiirepos = pygame.mouse.get_pos()
            #vaatab kas hiir ekraanil
            if hiirepos[0] < k.ekraani_laius and hiirepos[1] < k.ekraani_pikkus:
                #clear kahuri selection
                selected_kahur = None
                clear_select()
                if kahur_paigaldus == True:
                    loo_relv(hiirepos)
                else:
                    selected_kahur = select_kahur(hiirepos)
    
    #uuendab ekraani
    pygame.display.flip()
            
            
pygame.quit()