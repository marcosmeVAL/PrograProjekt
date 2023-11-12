import pygame
import mängu_constant as c
import json
from enemy import Enemy
from world import World
from turret import Turret

pygame.init()

#clock
clock = pygame.time.Clock()

#ekraan

screen = pygame.display.set_mode((c.SCREEN_LAIUS, c.SCREEN_PIKKUS))
pygame.display.set_caption("TTD")


#load img
#mapp
map_image = pygame.image.load("mappid\level.png").convert_alpha() #mapp vaja lisada

#enemies
enemy_image = pygame.image.load("vaenlane.png").convert_alpha() #vaenlased vaja lisada

#indiv turret img
cursor_turret = pygame.image.load("cursor_turret.png").convert_alpha() #turretid vaja lisada

#load json

with open("mappid\level.tmj") as fail:
    world_data = json.load(fail)
    

    
#maailm
world = World(world_data, map_image)
world.process_data()



#gruppid
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()


enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

#funktsioonid
def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #calc the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    #check if tile'i peale saab panna turreti
    if world.tile_map[mouse_tile_num] == "7":
        #chceck if turret there
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False 
        #if ruumi on
        if space_is_free == True:
            new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)
            
            
#mängu loop
run = True
while run:
    #FPS
    clock.tick(c.FPS)
    
    screen.fill("black")
    #draw level
    world.draw(screen)
    
    #DRAW ENEMY PATH prg näiteks 

    
    #update gruppid
    enemy_group.update()
    
    
    #gruppide joonistamine
    enemy_group.draw(screen)
    turret_group.draw(screen)
    print(turret_group)
    
    #evendid
    for event in pygame.event.get():
        #kinni panemiseks
        if event.type == pygame.QUIT:
            run = False
        #mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            #check if mouse in ekraan
            if mouse_pos[0] < c.SCREEN_LAIUS and mouse_pos[1] < c.SCREEN_PIKKUS:    
                create_turret(mouse_pos)
            
    #update
    pygame.display.flip()
    


pygame.quit()