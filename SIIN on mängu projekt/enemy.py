import pygame
from pygame.math import Vector2
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, image):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.angle = 0
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.original_img = image
        
    def update(self):
        self.move()
        self.rotate()
    
    def move(self):
        #def target
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #lõpp
            self.kill()
        
        #calc distance to target
        dist = self.movement.length()
        #check if remaining distance is suurem kui enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1
        
    def rotate(self):
        #arvuta dist järgmise waypontini
        dist = self.target - self.pos
        #use dist calc nurk
        self.angle = math.degrees(math.atan2(dist[1], dist[0]))
        #rotate img ja update rectangle(truut)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos