import pygame
import mängu_constant

class Turret(pygame.sprite.Sprite):
    def __init__(self, imagem, tile_x, tile_y):
        pygame.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y
        #calc center kordinaadid
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)