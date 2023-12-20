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
mäng_läbi = False
mäng_outcome = 0 #1 võit / -1 kaotus
viim_vaenlase_spawn = pygame.time.get_ticks()
kahur_paigaldus = False
kahur1_paigaldus = False
selected_kahur = None
level_start = False 

#laeb erinevaid pilte
#vaenlased
vaenlaste_pildid = {"lev1": pygame.image.load("ülejäänudassetid/v1.png").convert_alpha(),
                    "lev2": pygame.image.load("ülejäänudassetid/v2.png").convert_alpha(),
                    "lev3": pygame.image.load("ülejäänudassetid/v3.png").convert_alpha(),
                    "lev4": pygame.image.load("ülejäänudassetid/v4.png").convert_alpha()
                    }
#vaenlane_pilt = pygame.image.load("ülejäänudassetid/enemy_1.png").convert_alpha()
#kaart
kaart = pygame.image.load("mappid/ProjektiMapp.png").convert_alpha()

#kahurid
kahuri_sheetid = []
kahuri1_sheetid = []

for i in range(1, k.kahur_levels + 1):
    kahuri_sheet = pygame.image.load(f"pildid/turret_{i}.png").convert_alpha()
    kahuri_sheetid.append(kahuri_sheet)

for e in range(1, k.kahur_levels + 1):
    kahuri1_sheet = pygame.image.load(f"pildid/kahur1sheet{e}.png").convert_alpha()
    kahuri1_sheetid.append(kahuri1_sheet)
    
#hiirekahur
hiirekahur = pygame.image.load("pildid/kahur1.png").convert_alpha()
hiirekahur1 = pygame.image.load("pildid/hiirekahur.png").convert_alpha()

#nupud mängu akna kõrval
kahuri_ostmisnupp = pygame.image.load("pildid/kahur.png").convert_alpha()
kahuri1_ostmisnupp = pygame.image.load("pildid/kahur2.png").convert_alpha()
cancel_pilt = pygame.image.load("pildid/can.png").convert_alpha()
upg_kahur_pilt = pygame.image.load("pildid/uuenda.png").convert_alpha()
alga_level = pygame.image.load("pildid/alusta.png").convert_alpha()
restart = pygame.image.load("pildid/resa.png").convert_alpha()
kiirenda = pygame.image.load("pildid/ff.png").convert_alpha()

sydamepilt = pygame.image.load("pildid/süda.png").convert_alpha()
rahapilt = pygame.image.load("pildid/coinpic.png").convert_alpha()
ppic = pygame.image.load("pildid/KMLOGO.png").convert_alpha()
ppic = pygame.transform.scale(ppic, (300, 320))
#

#Gruppid

vaenlane_grupp = pygame.sprite.Group()
kahuri_grupp = pygame.sprite.Group()
kahuri1_grupp = pygame.sprite.Group()

#Json info
with open("mappid/ProjektiMapp.tmj") as fail:
    maailm_info = json.load(fail)
#Maailm
maailm = Maailm(maailm_info, kaart)
maailm.protsess_info()
maailm.vaenlased_p()

#fontid
teksti_font = pygame.font.SysFont("Consolas", 24, bold=True)
teksti_suur_font = pygame.font.SysFont("Consolas", 36)

def tekst(tekst, font, värv, x, y):
    img = font.render(tekst, True, värv)
    ekraan.blit(img, (x, y))
def ekraan_data():
    pygame.draw.rect(ekraan, "mediumslateblue", (k.ekraani_laius, 0, k.kõrval_paneel, k.ekraani_pikkus))
    pygame.draw.rect(ekraan, "grey", (k.ekraani_laius, 0, k.kõrval_paneel, 400), 2)
    ekraan.blit(ppic, (k.ekraani_laius, 400))
    #
    ekraan.blit(sydamepilt, ( k.ekraani_laius + 10, 5))
    tekst(str(maailm.elud), teksti_font, "black", k.ekraani_laius + 50, 10)
    #
    ekraan.blit(rahapilt, ( k.ekraani_laius + 10, 35))
    tekst(str(maailm.money), teksti_font, "black", k.ekraani_laius + 50, 40)
    #
    tekst("Level: " + str(maailm.level), teksti_font, "black", 0, 10)
    
    
#loo nupp
kahuri_nupp = Nupp(k.ekraani_laius + 30, 130, kahuri_ostmisnupp, True)
kahuri1_nupp = Nupp(k.ekraani_laius + 30, 190, kahuri1_ostmisnupp, True)
cancel_nupp = Nupp(k.ekraani_laius + 50, 250, cancel_pilt, True)
upg_nupp = Nupp(k.ekraani_laius + 30, 70, upg_kahur_pilt, True)
alga_nupp = Nupp(k.ekraani_laius + 60, 320, alga_level, True)
resa_nupp = Nupp(310, 300, restart, True)
kiirenda_nupp = Nupp(k.ekraani_laius + 50, 320, kiirenda, False)

#funktsioonid
def loo_relv(hiirepos):
    hiire_koord_x = hiirepos[0] // k.ruut
    hiire_koord_y = hiirepos[1] // k.ruut
    hiir = (hiire_koord_y * k.veerg) + hiire_koord_x
    #proovi kaardil/mappil on muru id 7
    if maailm.kaardi_ruut[hiir] == 1:
        ruum_vaba = True
        for kahur in kahuri_grupp:
            if (hiire_koord_x, hiire_koord_y) == (kahur.x_koordinaat, kahur.y_koordinaat):
                ruum_vaba = False
        if ruum_vaba == True:
            ukahur = Kahur(kahuri_sheetid, hiire_koord_x, hiire_koord_y)
            kahuri_grupp.add(ukahur)
            #võta raha
            maailm.money -= k.kahuri_ost
            
def loo_relv1(hiirepos):
    hiire_koord_x = hiirepos[0] // k.ruut
    hiire_koord_y = hiirepos[1] // k.ruut
    hiir = (hiire_koord_y * k.veerg) + hiire_koord_x
    #proovi kaardil/mappil on muru id 7
    if maailm.kaardi_ruut[hiir] == 1:
        ruum_vaba = True
        for kahur1 in kahuri1_grupp:
            if (hiire_koord_x, hiire_koord_y) == (kahur1.x_koordinaat, kahur1.y_koordinaat):
                ruum_vaba = False
        if ruum_vaba == True:
            ukahur1 = Kahur(kahuri1_sheetid, hiire_koord_x, hiire_koord_y)
            kahuri1_grupp.add(ukahur1)
            #võta raha
            maailm.money -= k.kahuri_ost
            
def clear_select():
    for kahur in kahuri_grupp:
        kahur.selected = False
    for kahur1 in kahuri1_grupp:
        kahur1.selected = False
        
def select_kahur(hiirepos):
    hiire_koord_x = hiirepos[0] // k.ruut
    hiire_koord_y = hiirepos[1] // k.ruut
    for kahur in kahuri_grupp:
        if (hiire_koord_x, hiire_koord_y) == (kahur.x_koordinaat, kahur.y_koordinaat):
            return kahur
    for kahur1 in kahuri1_grupp:
        if (hiire_koord_x, hiire_koord_y) == (kahur1.x_koordinaat, kahur1.y_koordinaat):
            return kahur1

# run-ile saab anda väärtuse False, et mängu kinni panna
run = True
#mängu loop e. mäng
while run:
    
    clock.tick(k.FPS)
    ekraan.fill("white")
    #UPDATID
    #uuendame gruppe pilte (vaenlase juures asukohta)
    if mäng_läbi == False:
        #vaata kas kaotus
        if maailm.elud <= 0:
            mäng_läbi = True
            mäng_outcome = -1
        #vaata kas võit
        if maailm.level > k.totallevels:
            mäng_läbi = True
            mäng_outcome = 1
            
        vaenlane_grupp.update(maailm)
        kahuri_grupp.update(vaenlane_grupp, maailm)
        kahuri1_grupp.update(vaenlane_grupp, maailm)
        #
        if selected_kahur:
            selected_kahur.selected = True
    
    
    #JOONESTAMISED
    #joonistab kaardi
    maailm.draw(ekraan)
    
    #joonistab vaenlaste tee praegu näiteks
    #pygame.draw.lines(ekraan, "black", False, maailm.sihid)
    
    ekraan_data()
    
    
    if mäng_läbi == False:           
        #ekraanile joonistamine
        vaenlane_grupp.draw(ekraan)
        for kahur in kahuri_grupp:
            kahur.draw(ekraan)
        for kahur1 in kahuri1_grupp:
            kahur1.draw(ekraan)
        #vaaata kas lev on alatud 
        #vaenlaste spawn
        if level_start == False:
            if alga_nupp.draw(ekraan):
                level_start = True
        else:
            #ff
            maailm.mängkiirus = 1
            if kiirenda_nupp.draw(ekraan):
                maailm.mängkiirus = 2
            if pygame.time.get_ticks() - viim_vaenlase_spawn > k.spawni_cd / maailm.mängkiirus:
                if maailm.spawned < len(maailm.vaenlaste_l):
                    vaenlase_tugevus = maailm.vaenlaste_l[maailm.spawned]
                    vaenlane = Vaenlane(vaenlase_tugevus, maailm.sihid, vaenlaste_pildid)
                    vaenlane_grupp.add(vaenlane)
                    maailm.spawned += 1
                    viim_vaenlase_spawn = pygame.time.get_ticks()
                    
        if maailm.vaata_levelit() == True:
            maailm.money += k.level_lõpp_rew
            maailm.level += 1
            level_start = False
            viim_vaenlase_spawn = pygame.time.get_ticks()
            maailm.reset_level()
            maailm.vaenlased_p()
                    
        #ekraani kõrval paneel
        #nupu joonistamine
        ekraan.blit(rahapilt, ( k.ekraani_laius + 260, 135))
        ekraan.blit(rahapilt, ( k.ekraani_laius + 260, 195))
        tekst(str(k.kahuri_ost), teksti_font, "black", k.ekraani_laius + 215,  135)
        tekst(str(k.kahuri_ost), teksti_font, "black", k.ekraani_laius + 215,  195)
        if kahuri_nupp.draw(ekraan):
            kahur_paigaldus = True
        if kahuri1_nupp.draw(ekraan):
            kahur1_paigaldus = True 
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
                
        if kahur1_paigaldus == True:
            #näite kahurrit hiirel
            cursor_rect = hiirekahur1.get_rect()
            curser_pos = pygame.mouse.get_pos()
            cursor_rect.center = curser_pos
            
            if curser_pos[0] <= k.ekraani_laius:
                ekraan.blit(hiirekahur1, cursor_rect)
                
            if cancel_nupp.draw(ekraan):
                kahur1_paigaldus = False 
        #upgrade nupp
        if selected_kahur:
            if selected_kahur.upg_level < k.kahur_levels:
                if upg_nupp.draw(ekraan):
                    if maailm.money >= k.kahuri_upgrade:
                        selected_kahur.upgrade() 
                        maailm.money -= k.kahuri_upgrade
        
    else:
        pygame.draw.rect(ekraan, "pink", (200, 200, 400, 200), border_radius = 30)
        if mäng_outcome == -1:
            tekst("GAME OVER", teksti_suur_font, "black", 310, 230)
        elif mäng_outcome == 1:
            tekst("YOU WIN", teksti_suur_font, "black", 320, 230)
        #resa lev
        if resa_nupp.draw(ekraan):
            mäng_läbi = False
            level_start = False
            kahur_paigaldus = False
            kahur1_paigaldus = False
            selected_kahur = None
            viim_vaenlase_spawn = pygame.time.get_ticks()
            maailm = Maailm(maailm_info, kaart)
            maailm.protsess_info()
            maailm.vaenlased_p()
            #tühjenda kõik
            vaenlane_grupp.empty()
            kahuri_grupp.empty()
                
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
                    #raha
                    if maailm.money >= k.kahuri_ost:
                        loo_relv(hiirepos)
                if kahur1_paigaldus == True:
                    #raha
                    if maailm.money >= k.kahuri_ost:
                        loo_relv1(hiirepos)
                else:
                    selected_kahur = select_kahur(hiirepos)
    
    #uuendab ekraani
    pygame.display.flip()
            
            
pygame.quit()