import pygame
from vaenlase_data import Vspawn_data
import random
import mängu_kindlad_seaded as k

class Maailm():
    def __init__(self, info, kaart):
        self.level = 1
        self.elud = k.Elud
        self.money = k.Cash
        self.kaardi_ruut = []
        self.sihid = []
        self.taseme_info = info
        self.image = kaart
        self.vaenlaste_l = []
        self.spawned = 0
        self.killedv = 0
        self.missedv = 0
    
    def protsess_info(self):
        #otsib kasulikku infot
        for kiht in self.taseme_info["layers"]:
            
            if kiht["name"] == "tilemap":
                self.kaardi_ruut = kiht["data"]
                
            elif kiht["name"] == "waypoints":
                for objekt in kiht["objects"]:
                    waypoint_info = objekt["polyline"]
                    self.protsess_sihid(waypoint_info)
                    
    def vaenlased_p(self):
        vaen = Vspawn_data[self.level - 1]
        for vaenlasetüüp in vaen:
            vaelasedspawnivad = vaen[vaenlasetüüp]
            for v in range(vaelasedspawnivad):
                self.vaenlaste_l.append(vaenlasetüüp)
        #sega vaenlaste listi
        random.shuffle(self.vaenlaste_l)
        
    def vaata_levelit(self):
        if (self.killedv + self.missedv) == len(self.vaenlaste_l):
            return True
        
    def reset_level(self):
        self.vaenlaste_l = []
        self.spawned = 0
        self.killedv = 0
        self.missedv = 0
        
    def protsess_sihid(self, info):
        
        for i in info:
            ajutx = i.get("x")
            ajuty = i.get("y")
            self.sihid.append((ajutx, ajuty))
            
                
    def draw(self, surface):
        surface.blit(self.image, (0, 0))