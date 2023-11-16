import pygame
import mängu_kindlad_seaded as k


class Kahur(pygame.sprite.Sprite):
    def __init__(self, image, x_koordinaat, y_koordinaat):
        pygame.sprite.Sprite.__init__(self)
        self.x_koordinaat = x_koordinaat
        self.y_koordinaat = y_koordinaat
        #arvutab ruudu keskpunktiä
        self.x = (self.x_koordinaat + 0.5) * k.ruut
        self.y = (self.y_koordinaat + 0.5) * k.ruut
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)