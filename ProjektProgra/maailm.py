import pygame

class Maailm():
    def __init__(self, info, kaart):
        self.kaardi_ruut = []
        self.sihid = []
        self.taseme_info = info
        self.image = kaart
    
    def protsess_info(self):
        #otsib kasulikku infot
        for kiht in self.taseme_info["layers"]:
            
            if kiht["name"] == "tilemap":
                self.kaardi_ruut = kiht["data"]
                
            elif kiht["name"] == "waypoints":
                for objekt in kiht["objects"]:
                    waypoint_info = objekt["polyline"]
                    self.protsess_sihid(waypoint_info)
                    
    def protsess_sihid(self, info):
        
        for i in info:
            ajutx = i.get("x")
            ajuty = i.get("y")
            self.sihid.append((ajutx, ajuty))
            
                
    def draw(self, surface):
        surface.blit(self.image, (0, 0))