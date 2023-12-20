import pygame


class Nupp():
    def __init__(self, x, y, image, singel_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.singel_click = singel_click
    
    def draw(self, surface):
        action = False
        
        #hiire pos
        pos = pygame.mouse.get_pos()
           
        
        #hiire kontroll
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                #kui nup ainuclickimis tyypi, ss clicked annab väärtuse True
                if self.singel_click:
                    self.clicked = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        #joonesta nupp
        surface.blit(self.image, self.rect)
        return action