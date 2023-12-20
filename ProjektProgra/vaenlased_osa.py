import pygame
from pygame.math import Vector2
import math
from vaenlase_data import VaenData
import mängu_kindlad_seaded as k

class Vaenlane(pygame.sprite.Sprite):
    def __init__(self, vaenlase_tugevus, waypoints, images):
        
        pygame.sprite.Sprite.__init__(self)
        #
        self.waypoints = waypoints
        #
        self.positsioon = Vector2(self.waypoints[0])
        #
        self.siht_waypoint = 0
        #
        self.elu = VaenData.get(vaenlase_tugevus)["elu"]
        #
        self.kiirus = VaenData.get(vaenlase_tugevus)["kiirus"]
        #
        self.org_image = images.get(vaenlase_tugevus)
        #
        self.nurk = 0
        #
        self.image = pygame.transform.rotate(self.org_image, self.nurk)
        #
        self.rect = self.image.get_rect()
        #
        self.rect.center = self.positsioon
        #
    
    def vaata_elusi(self, maailm):
        if self.elu <= 0:
            maailm.money += k.kill_rew
            maailm.killedv += 1
            self.kill()
        
    def liikumine(self, maailm):
        #otsi uus siht kuhu liikuda
        if self.siht_waypoint < len(self.waypoints):
            self.siht = Vector2(self.waypoints[self.siht_waypoint])
            self.liikuma = self.siht - self.positsioon
        else:
            #rohkem waypointe pole
            self.kill()
            maailm.elud -= 1
            maailm.missedv += 1
            
        #arvuta kaugus sihist
        dist = self.liikuma.length()
        #vaatab palju sihini on
        if dist >= (self.kiirus * maailm.mängkiirus):
            self.positsioon += self.liikuma.normalize() * (self.kiirus * maailm.mängkiirus)
        else:
            if dist != 0:    
                self.positsioon += self.liikuma.normalize() * dist
            self.siht_waypoint += 1
            
        #self.rect.center = self.positsioon
        
        
    def update(self, maailm):
        self.liikumine(maailm)
        self.pööra()
        self.vaata_elusi(maailm)
        
    def pööra(self):
        #arvutab kauguse järgmise waypointini
        dist = self.siht - self.positsioon
        #kasutab kaugust, et arvutada nurga
        self.nurk = math.degrees(math.atan2(-dist[1], dist [0]))
        #pöörab pilti
        self.image = pygame.transform.rotate(self.org_image, self.nurk)
        self.rect = self.image.get_rect()
        self.rect.center = self.positsioon