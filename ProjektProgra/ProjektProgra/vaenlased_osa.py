import pygame
from pygame.math import Vector2
import math


class Vaenlane(pygame.sprite.Sprite):
    def __init__(self, waypoints, image):
        
        pygame.sprite.Sprite.__init__(self)
        #
        self.waypoints = waypoints
        #
        self.positsioon = Vector2(self.waypoints[0])
        #
        self.siht_waypoint = 1
        #
        self.kiirus = 2
        #
        self.org_image = image
        #
        self.nurk = 0
        #
        self.image = pygame.transform.rotate(self.org_image, self.nurk)
        #
        self.rect = self.image.get_rect()
        #
        self.rect.center = self.positsioon
        #
        
        
    def liikumine(self):
        #otsi uus siht kuhu liikuda
        if self.siht_waypoint < len(self.waypoints):
            self.siht = Vector2(self.waypoints[self.siht_waypoint])
            self.liikuma = self.siht - self.positsioon
        else:
            #rohkem waypointe pole
            self.kill()
            
        #arvuta kaugus sihist
        dist = self.liikuma.length()
        #vaatab palju sihini on
        if dist >= self.kiirus:
            self.positsioon += self.liikuma.normalize() * self.kiirus
        else:
            if dist != 0:    
                self.positsioon += self.liikuma.normalize() * dist
            self.siht_waypoint += 1
            
        #self.rect.center = self.positsioon
        
        
    def update(self):
        self.liikumine()
        self.pööra()
        
        
    def pööra(self):
        #arvutab kauguse järgmise waypointini
        dist = self.siht - self.positsioon
        #kasutab kaugust, et arvutada nurga
        self.nurk = math.degrees(math.atan2(-dist[1], dist [0]))
        #pöörab pilti
        self.image = pygame.transform.rotate(self.org_image, self.nurk)
        self.rect = self.image.get_rect()
        self.rect.center = self.positsioon