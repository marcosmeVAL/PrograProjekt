import pygame
import mängu_kindlad_seaded as k
import math
from kahuri_data import KDATA


class Kahur(pygame.sprite.Sprite):
    def __init__(self, sprite_sheets, x_koordinaat, y_koordinaat):
        pygame.sprite.Sprite.__init__(self)
        #
        self.upg_level = 1
        self.range = KDATA[self.upg_level - 1].get("range")
        #cd tähendab cooldown
        self.cd = KDATA[self.upg_level - 1].get("cd")
        self.last_shot = pygame.time.get_ticks()
        self.selected = False
        self.sihtmärk = None
        
        #
        self.x_koordinaat = x_koordinaat
        self.y_koordinaat = y_koordinaat
        #arvutab ruudu keskpunktiä
        self.x = (self.x_koordinaat + 0.5) * k.ruut
        self.y = (self.y_koordinaat + 0.5) * k.ruut
        #animatsioon
        self.sprite_sheets = sprite_sheets
        self.animatioon_list = self.lae_pildid(self.sprite_sheets[self.upg_level - 1])
        self.frame_indeks = 0
        self.update_time = pygame.time.get_ticks()
        #update pilt
        self.nurk = 90
        self.image_og = self.animatioon_list[self.frame_indeks]
        self.image = pygame.transform.rotate(self.image_og, self.nurk)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        #kaugus
        self.range_img = pygame.Surface((self.range * 2, self.range * 2))
        self.range_img.fill(( 0, 0, 0))
        self.range_img.set_colorkey(( 0, 0, 0))
        pygame.draw.circle(self.range_img, "grey", (self.range, self.range), self.range)
        self.range_img.set_alpha(100)
        self.range_rect = self.range_img.get_rect()
        self.range_rect.center = self.rect.center
        
    def lae_pildid(self, sprite_sheet):
        ###võtab pildid sprite sheetist
        suurus = sprite_sheet.get_height()
        anim_list = []
        for i in range(k.animatsioon_protsess):
            ajut_img = sprite_sheet.subsurface( i * suurus, 0, suurus, suurus)
            anim_list.append(ajut_img)
        return anim_list
    
    def update(self, vaenlane_grupp):
        #sihtm ss reageeri
        if self.sihtmärk:
            self.animatsioon()
        else:
            #otsi uus sihtmärk
            if pygame.time.get_ticks() - self.last_shot > self.cd:
                self.sihtmärgid(vaenlane_grupp)
                
    def upgrade(self):
        self.upg_level += 1
        self.range = KDATA[self.upg_level - 1].get("range")
        self.cd = KDATA[self.upg_level - 1].get("cd")
        #upgrade pildid
        self.animatioon_list = self.lae_pildid(self.sprite_sheets[self.upg_level - 1])
        self.image_og = self.animatioon_list[self.frame_indeks]
        
        #upg range ring
        self.range_img = pygame.Surface((self.range * 2, self.range * 2))
        self.range_img.fill(( 0, 0, 0))
        self.range_img.set_colorkey(( 0, 0, 0))
        pygame.draw.circle(self.range_img, "grey", (self.range, self.range), self.range)
        self.range_img.set_alpha(100)
        self.range_rect = self.range_img.get_rect()
        self.range_rect.center = self.rect.center
            
    def sihtmärgid(self, vaenlane_grupp):
        #leia vastane
        x_dist = 0
        y_dist = 0
        #vaata kaugust vastasest
        for v in vaenlane_grupp:
            if v.elu > 0:
                x_dist = v.positsioon[0] - self.x
                y_dist = v.positsioon[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.sihtmärk = v
                    self.nurk = math.degrees(math.atan2(-y_dist, x_dist))
                    self.sihtmärk.elu -= k.damg
                    break 
                
    def animatsioon(self):
        #update img
        self.image_og = self.animatioon_list[self.frame_indeks]
        #vaata kuna viimane update
        if pygame.time.get_ticks() - self.update_time > k.animatsioon_delay:
            self.update_time = pygame.time.get_ticks()
            self.frame_indeks += 1
            if self.frame_indeks >= len(self.animatioon_list):
                self.frame_indeks = 0
                self.last_shot = pygame.time.get_ticks()
                self.sihtmärk = None 
                
                
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.image_og, self.nurk - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_img, self.range_rect)
        
        
        
        
        
        
    