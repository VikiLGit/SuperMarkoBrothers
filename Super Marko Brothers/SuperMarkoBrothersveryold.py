#the code goes here

#pygamen tuontis
import pygame, csv

#pygamen initialisaatio
pygame.init()
pygame.mixer.init()
is_running = True
lives = 3
level = 1
score = 0
polo_murderer = False
marko_murderer = False

#näytön asetuksia

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#ikkunan nimi
pygame.display.set_caption("Super Marko Brothers")
#ikkunan kuvake
pygame.display.set_icon(pygame.image.load('smb_ico.png'))
#fontti
font =pygame.font.Font('freesansbold.ttf', 32)
fontxl =pygame.font.Font('freesansbold.ttf', 100)


jump_sound = pygame.mixer.Sound("sound/jump.wav")
jump_sound.set_volume(0.01)
taco_sound = pygame.mixer.Sound("sound/taco_sound.wav")
taco_sound.set_volume(0.05)
while is_running:
    has_killed = False
    #pelin elollisten olijoiden attributejen tallennukseen käytettävä classi
    class Attribute:
        def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float,character, x_pos:float, y_pos:float,hiding:bool,can_climb:bool,can_jump:bool,jump_time:int,jump:int,max_jump:int):
            self.y_velocity = y_velocity
            self.x_velocity = x_velocity
            self.on_ground = on_ground
            self.speed = speed
            self.character = character
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,80,80)
            #=============
            self.can_climb = can_climb
            self.hiding = hiding
            #=============
            self.can_jump = can_jump
            self.jump_time = jump_time
            self.jump = jump
            self.max_jump = max_jump
            self.alive = True
            self.frameid = 0
            self.delay = 0
            self.frame_count = 4

        def update_velocity(self, x_delta, y_delta):
            if self.y_velocity > 9:
                self.y_velocity = 9
            else:
                self.y_velocity += y_delta
            self.x_velocity = self.x_velocity / x_delta
            
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            
            self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,80,80)

            


        def camera(self):
            global global_x_offset
            global global_y_offset
            
            if self.x_pos >= 400:
                self.x_pos = 399
                if self.x_velocity > 0:
                    global_x_offset -= self.x_velocity
                else:
                    global_x_offset += self.x_velocity
            if self.y_pos <= 50:
                self.y_pos = 49
                global_y_offset -= self.y_velocity
            if (self.y_pos >= 50) and (not global_y_offset < 1):
                self.y_pos = 50
                global_y_offset -= self.y_velocity
            if global_y_offset <= 0:
                global_y_offset = 0
            if self.x_pos <= 0:
                self.x_pos = 0
                self.x_velocity = 0                                   
            if self.x_pos >= 800:
                self.x_pos = 799
        def movement(self):
            global global_x_offset
            self.delay += 1
            if self.delay == 6:
                self.frameid += 1
                self.delay = 0
                if self.frameid >= self.frame_count:
                    self.frameid = 0
            

            #pelaajan syötteet
            key = pygame.key.get_pressed()
            #pelaajan paikannus(test)
            if key[pygame.K_l]:
                print((self.x_pos-global_x_offset)//80*80,(self.y_pos-global_y_offset)//80*80+40)
            if self.on_ground:
                self.can_jump = True
                self.jump_time = 0
            elif 0 < self.jump_time < self.max_jump:
                self.can_jump = True
                
            else:
                self.on_ground = False
                self.can_jump = False
                self.can_climb = True
    
            #kiipeäminen
            if (key[pygame.K_r] == True) and (self.can_climb == True):
                self.y_velocity = 0
                screen.blit(self.character[7],(self.x_pos,self.y_pos))
            elif (key[pygame.K_s] == True) and (self.can_jump == True):
                if self.x_velocity > 0:
                    screen.blit(self.character[4], (self.x_pos, self.y_pos))
                    self.hiding = True
                elif self.x_velocity < 0:
                    screen.blit(pygame.transform.flip(self.character[4],True,False),(self.x_pos,self.y_pos))
                    self.hiding = True

            #hyppiminen
            elif (key[pygame.K_w] == True) and (self.can_jump == True):
                self.y_velocity = self.jump
                self.jump_time += 1
                jump_sound.play()
                self.hiding = False
                if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
                    screen.blit(self.character[5],(self.x_pos,self.y_pos))
                elif key[pygame.K_a] == True:
                    self.x_velocity += -self.speed
                    screen.blit(pygame.transform.flip(self.character[5],True,False),(self.x_pos,self.y_pos))
                elif key[pygame.K_d] == True:
                    self.x_velocity += self.speed
                    screen.blit(self.character[5],(self.x_pos,self.y_pos))
                else:
                    screen.blit(self.character[5],(self.x_pos,self.y_pos))
            elif (self.jump_time > 0) and (self.can_jump):
                self.jump_time += self.max_jump + 100
                screen.blit(self.character[5],(self.x_pos,self.y_pos))
                self.hiding = False   
            #kävely
            elif (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
                screen.blit(self.character[0],(self.x_pos,self.y_pos))
                self.hiding = False
            elif key[pygame.K_a] == True:
                self.x_velocity += -self.speed
                screen.blit(pygame.transform.flip(self.character[self.frameid],True,False),(self.x_pos,self.y_pos))
                self.hiding = False
            elif key[pygame.K_d] == True:
                self.x_velocity += self.speed
                screen.blit(self.character[self.frameid],(self.x_pos,self.y_pos))
                self.hiding = False
            else:
                screen.blit(self.character[0],(self.x_pos,self.y_pos))
                self.hiding = False

    class Object:
        def __init__(self,width:int,height:int,texture,loot:str=None,can_walk_through=False):
            self.width = width
            self.height = height
            self.loot = loot
            self.texture = pygame.transform.scale(texture,(self.width,self.height))
            self.can_walk_through = can_walk_through
        def draw(self,lista:list,entities:list=None):
            global global_x_offset
            global touch
            
            for location in lista:
                screen.blit(self.texture,location)
                if player.alive:
                    if self.can_walk_through == False:
                        #osumat palikan päällä
                        if (location[1] < player.y_pos + 80 < location[1] +20) and (location[0]-80+10 < player.x_pos < location[0]+self.width-10):
                            player.y_pos = location[1] - self.height
                            player.y_velocity = 0
                            player.on_ground = True
                            touch = True

                        #osumat palikan alla
                        if (location[1] +self.height >= player.y_pos >= location[1] +self.height -20) and (location[0]-80+10 <= player.x_pos <= location[0]+self.width-10):
                            player.y_pos = location[1] +self.height
                            if not self.loot == None:
                                items.append(Item(type=f"{self.loot}",x_pos=location[0]-global_x_offset,y_pos=location[1]-80-global_y_offset))
                                self.loot = None

                        #osumat palikan vasen laita
                        if (location[0] <= player.x_pos+80 <= location[0] +20) and (location[1]+10 <= player.y_pos +80 <= location[1]+self.height+80-10):
                            player.x_pos = location[0] -80

                        #osumat palikan oikea laita
                        if (location[0] + self.width >= player.x_pos >= location[0]-20) and (location[1]+10 <= player.y_pos +80 <= location[1]+self.height+80-10):
                            player.x_pos = location[0] +self.width

                if not entities == None:
                #npc osumat        
                    for entity in entities:
                        for location in lista:
                            #osumat palikan päällä
                            if (location[1] < entity.y_pos + 80+global_y_offset < location[1] +20) and (location[0]-80 < entity.x_pos + global_x_offset < location[0]+self.width):
                                entity.y_pos = location[1] - self.height -global_y_offset
                                entity.y_velocity = 0


                            #osumat palikan alla
                            if (location[1] +self.height >= entity.y_pos+global_y_offset >= location[1] +self.height -20) and (location[0]-80 <= entity.x_pos + global_x_offset <= location[0]+self.width):
                                entity.y_pos = location[1] +self.height -global_y_offset

                            #osumat palikan vasen laita
                            if (location[0] <= entity.x_pos + global_x_offset+80 <= location[0] +20) and (location[1]+10 <= entity.y_pos+global_y_offset +80 <= location[1]+self.height+80-10):
                                entity.x_pos = location[0] -80 -global_x_offset
                                if entity.x_velocity > 0:
                                    entity.x_velocity = -entity.x_velocity
                                
                            #osumat palikan oikea laita
                            if (location[0] + self.width >= entity.x_pos + global_x_offset >= location[0]-20) and (location[1]+10 <= entity.y_pos+global_y_offset +80 <= location[1]+self.height+80-10):
                                entity.x_pos = location[0] +self.width - global_x_offset
                                if entity.x_velocity < 0:
                                    entity.x_velocity = -entity.x_velocity
                               
    class Enemy:        
        def __init__(self, y_velocity:float, x_velocity:float,x_pos:int,y_pos:int, frame_count:int, anim_speed:int, type:str):
            self.y_velocity = y_velocity
            self.x_velocity = x_velocity
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.frameid = 0
            self.delay = 0
            self.anim_speed = anim_speed
            self.frame_count = frame_count
            self.character = eval(f"{type}_frames")
            self.rect = pygame.rect.Rect(self.x_pos+10+global_x_offset,self.y_pos+global_y_offset+10,60,60)
            self.type = type
            self.flip = False
        def update(self,y_delta:float):
            if self.y_velocity > 9:
                self.y_velocity = 9
            else:
                self.y_velocity += y_delta
            
            
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            
            self.rect = pygame.rect.Rect(self.x_pos+10+global_x_offset,self.y_pos+global_y_offset+10,60,60)
            
            self.delay += 1
            if self.delay == self.anim_speed:
                self.frameid += 1
                self.delay = 0
                if self.frameid >= self.frame_count:
                    self.frameid = 0
            if self.x_velocity <= 0:
                screen.blit(pygame.transform.flip(self.character[self.frameid],False,self.flip),(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
            else:
                screen.blit(pygame.transform.flip(self.character[self.frameid],True,self.flip),(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
            
    class Item:
        def __init__(self,type:str,x_pos:int,y_pos:int):
            self.type = type
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.texture = pygame.transform.scale(pygame.image.load(f'items/{type}.png').convert_alpha(),(80,80))
            self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,80,80)
        
        def draw(self):
            screen.blit(self.texture,(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
            self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,80,80)


    def drawer(level:int,entities:list,items:list):
        global lives
        global run
        global current_level_score
        global win
        global food

        #items
        collect = []
        for item in items:
            if pygame.Rect.colliderect(item.rect,player.rect):
                collect.append(item)
                if item.type == "bucket":
                    win = True
                elif item.type == "taco":
                    taco_sound.play()
                    food += 1000
                    
                elif item.type == "sauce":
                    lives += 1
        for take in collect:
            items.remove(take)
        for item in items:
            if (item.x_pos <= -global_x_offset + 800):
                item.draw()
                




        ded = []
        # npc kuolemat ja tapot
        for entity in entities:
            if entity.y_pos >= 700:
                ded.append(entity)


            if entity.type == "doge":
                if (entity.x_pos + global_x_offset+5 <= player.x_pos+80 <= entity.x_pos +160+ global_x_offset-5) and (entity.y_pos+global_y_offset-80-20 <= player.y_pos <= entity.y_pos+global_y_offset-80): 
                    ded.append(entity)
                    player.y_velocity = player.jump
                    current_level_score += 100
                    has_killed = True
                elif pygame.Rect.colliderect(entity.rect,player.rect):
                    
                    player.alive = False 


            elif entity.type == "car":
                if (entity.x_pos + global_x_offset+10 <= player.x_pos+80 <= entity.x_pos +160+ global_x_offset-10) and (entity.y_pos+global_y_offset-80-20 <= player.y_pos <= entity.y_pos+global_y_offset-80): 
                    player.y_velocity = player.jump
                    if entity.flip == False:
                        entity.flip = True
                        current_level_score += 100
                        entity.x_velocity = entity.x_velocity *10
                    else:
                        entity.x_velocity = -entity.x_velocity
                    has_killed = True
                elif pygame.Rect.colliderect(entity.rect,player.rect) and player.alive and player.hiding == False:
                    player.alive = False



            for upsidedown in entities:
                if (upsidedown.flip == True) and (not upsidedown == entity):
                    if pygame.Rect.colliderect(entity.rect,upsidedown.rect):
                        if entity.flip == True:
                            ded.append(upsidedown)
                            current_level_score += 100
                        ded.append(entity)
                        current_level_score += 100
            for i in entities:
                if not i == entity and (not i.flip and not entity.flip):
                    #osumat olion päältä
                    if (i.y_pos + global_y_offset < entity.y_pos + 80 < i.y_pos + global_y_offset +20) and (i.x_pos + global_x_offset-80 < entity.x_pos + global_x_offset < i.x_pos + global_x_offset+80):
                        entity.y_pos = i.y_pos -80
                        entity.y_velocity = 0
                    #osumat olion alla
                    if (i.y_pos+ global_y_offset +80 >= entity.y_pos >= i.y_pos+ global_y_offset +80 -20) and (i.x_pos + global_x_offset-80 <= entity.x_pos + global_x_offset <= i.x_pos + global_x_offset+80):
                        entity.y_pos = i.y_pos +80

                    #osumat olion vasen laita
                    if (i.x_pos+ + global_x_offset <= entity.x_pos + global_x_offset+80 <= i.x_pos + global_x_offset +20) and (i.y_pos+10+global_y_offset <= entity.y_pos +80 <= i.y_pos+80+80-10+global_y_offset):
                        entity.x_pos = i.x_pos -80 
                        if entity.x_velocity > 0:
                            entity.x_velocity = -entity.x_velocity

                    #osumat polion oikea laita
                    if (i.x_pos + global_x_offset + 80 >= entity.x_pos + global_x_offset >= i.x_pos + global_x_offset-20) and (i.y_pos+10+global_y_offset <= entity.y_pos +80 <= i.y_pos+80+80-10+global_y_offset):
                        entity.x_pos = i.x_pos +80
                        if entity.x_velocity < 0:
                            entity.x_velocity = -entity.x_velocity
        for bury in ded:
            entities.remove(bury)
        for entity in entities:
            if not entity.x_pos >= -global_x_offset + 1000:
                entity.update(y_delta)

        if level == 1:
            global touch
            touch = False

            sand10x.draw([
                (global_x_offset,global_y_offset+520),
                (global_x_offset+800,global_y_offset+520),
                (global_x_offset+1840,global_y_offset+520),
                (global_x_offset+2880,global_y_offset+520),
                (global_x_offset+4000,global_y_offset+520),
                (global_x_offset+4800,global_y_offset+520),
                (global_x_offset+7200,global_y_offset+520)
                ],entities)
            
            sand.draw([
                (global_x_offset+5920,global_y_offset+520),
                (global_x_offset+6480,global_y_offset+520)
                ],entities)
            
            brick3x.draw([
                (global_x_offset+6640,global_y_offset+280),
                (global_x_offset+4560,global_y_offset+280)
                ],entities)
            
            brick.draw([
                (global_x_offset+2480,global_y_offset+440),
                (global_x_offset+2560,global_y_offset+440),
                (global_x_offset+2560,global_y_offset+360),
                (global_x_offset+6080,global_y_offset+280)
                ],entities)
            lootbox_taco.draw([
                (global_x_offset+320,global_y_offset+280)
            ],entities)
            well.draw([
                (global_x_offset+800,global_y_offset+440),
                (global_x_offset+1440,global_y_offset+440),
                (global_x_offset+1440,global_y_offset+360),
                (global_x_offset+1440,global_y_offset+280),
                (global_x_offset+1840,global_y_offset+440),
                (global_x_offset+1840,global_y_offset+360),
                (global_x_offset+1840,global_y_offset+280),
                (global_x_offset+3520,global_y_offset+440)
            ],entities)
            canopy.draw([
                (global_x_offset+800,global_y_offset+280),
                (global_x_offset+1440,global_y_offset+120),
                (global_x_offset+1840,global_y_offset+120),
                (global_x_offset+3520,global_y_offset+280)
            ],entities)
            if touch == False:
                player.on_ground = False
        elif level == 2:
            touch = False

            sand10x.draw([
                (global_x_offset+0,global_y_offset+520),
                (global_x_offset+800,global_y_offset+520),
                (global_x_offset+1840,global_y_offset+520),
                (global_x_offset+2880,global_y_offset+520),
                (global_x_offset+4000,global_y_offset+520),
                (global_x_offset+4800,global_y_offset+520),
                (global_x_offset+7200,global_y_offset+520)
                ],entities)
            
            sand.draw([
                (global_x_offset+5920,global_y_offset+520),
                (global_x_offset+6480,global_y_offset+520),
                (global_x_offset+1600,global_y_offset+520),
                (global_x_offset+1680,global_y_offset+520),
                (global_x_offset+1760,global_y_offset+520)
                
                ],entities)
            
            brick3x.draw([
                (global_x_offset+1600,global_y_offset+440),
                (global_x_offset+6640,global_y_offset+280),
                (global_x_offset+7280,global_y_offset+40),
                (global_x_offset+4560,global_y_offset+280)
                
                ],entities)
            
            brick.draw([
                (global_x_offset+2640,global_y_offset+520),
                (global_x_offset+6080,global_y_offset+280),
                (global_x_offset+7920,global_y_offset+440),
                (global_x_offset+7920,global_y_offset+520),
                (global_x_offset+7920,global_y_offset+360),
                (global_x_offset+7920,global_y_offset+280),
                (global_x_offset+7680,global_y_offset+200),
                (global_x_offset+7760,global_y_offset+200),
                (global_x_offset+7520,global_y_offset+280)
                
                ],entities)
            
            lootbox_taco.draw([
                (global_x_offset+7040,global_y_offset+280)
            ])
            lootbox_taco1.draw([
                (global_x_offset+7600,global_y_offset+200)
            ])

            well.draw ([
                (global_x_offset+2560,global_y_offset+440)
            ],entities)
            canopy.draw ([
                (global_x_offset+2560,global_y_offset+280)
            ])
            if touch == False:
                player.on_ground = False
        elif level == 3:
            touch = False

            sand10x.draw([
                (global_x_offset+0,global_y_offset+520),
                (global_x_offset+800,global_y_offset+520),
                (global_x_offset+1840,global_y_offset+520),
                
                (global_x_offset+4000,global_y_offset+520),
                (global_x_offset+4800,global_y_offset+520),
                (global_x_offset+7200,global_y_offset+520)
                ],entities)
            
            sand.draw([
                (global_x_offset+5520,global_y_offset+440),
                (global_x_offset+5920,global_y_offset+520),
                (global_x_offset+6160,global_y_offset+520),
                (global_x_offset+6480,global_y_offset+520)
                ],entities)
            
            brick3x.draw([
                (global_x_offset+1120, global_y_offset+280),
                (global_x_offset+2800,global_y_offset+520),
                (global_x_offset+4160,global_y_offset+440),
                (global_x_offset+4160,global_y_offset+280),
                (global_x_offset+4400,global_y_offset+440),
                (global_x_offset+4400,global_y_offset+280),
                (global_x_offset+6240,global_y_offset+280),
                (global_x_offset+6640,global_y_offset+280)
                ],entities)
            
            brick.draw([
                (global_x_offset+1200,global_y_offset+40),
                (global_x_offset+1360,global_y_offset-120),
                (global_x_offset+2480,global_y_offset+440),
                (global_x_offset+2560,global_y_offset+440),
                (global_x_offset+2560,global_y_offset+360),
                (global_x_offset+2960,global_y_offset+200),
                (global_x_offset+3040,global_y_offset+200),
                (global_x_offset+3520,global_y_offset+520),
                (global_x_offset+3600,global_y_offset+520),
                (global_x_offset+4160,global_y_offset+200),
                (global_x_offset+4160,global_y_offset+120),
                (global_x_offset+5920,global_y_offset+280),
                (global_x_offset+6000,global_y_offset+280)
                ],entities)
            lootbox_taco.draw([
                (global_x_offset+1280,global_y_offset+280)
            ],entities)
            well.draw([
                (global_x_offset+800,global_y_offset+440),
                (global_x_offset+1840,global_y_offset+440),
                (global_x_offset+1840,global_y_offset+360),
                (global_x_offset+1840,global_y_offset+280),
                (global_x_offset+1840,global_y_offset+200),
                (global_x_offset+3520,global_y_offset+440),
                (global_x_offset+4320,global_y_offset+200)
            
            ],entities)
            canopy.draw([
                (global_x_offset+800,global_y_offset+280),
                
                (global_x_offset+1840,global_y_offset+40),
                (global_x_offset+3520,global_y_offset+280),
                (global_x_offset+4320,global_y_offset+40)
            ],entities)
            if touch == False:
                player.on_ground = False
        elif level == 4:
            touch = False

            sand10x.draw([
                (global_x_offset+0,global_y_offset+520),
                (global_x_offset+800,global_y_offset+520),
                (global_x_offset+4000,global_y_offset+520),
                (global_x_offset+4800,global_y_offset+520),
                (global_x_offset+5600,global_y_offset+520),
                (global_x_offset+7200,global_y_offset+520),
                
                ],entities)
            
            sand.draw([

                (global_x_offset+1920,global_y_offset+520),
                (global_x_offset+2000,global_y_offset+520),
                (global_x_offset+2080,global_y_offset+520),
                (global_x_offset+2160,global_y_offset+520),
                (global_x_offset+2240,global_y_offset+520),
                (global_x_offset+3200,global_y_offset+520),
                (global_x_offset+3280,global_y_offset+520),
                (global_x_offset+3360,global_y_offset+520),
                (global_x_offset+3440,global_y_offset+520),
                (global_x_offset+3760,global_y_offset+520),
                (global_x_offset+6400,global_y_offset+520),
                (global_x_offset+6480,global_y_offset+520),
                (global_x_offset+7120,global_y_offset+520),
                ],entities)
            
            brick3x.draw([
                (global_x_offset+2560,global_y_offset+280),
                (global_x_offset+4720,global_y_offset+280),
                (global_x_offset+6640,global_y_offset+280),
                (global_x_offset+7520,global_y_offset+40),
                ],entities)
            
            brick.draw([
                (global_x_offset+1520,global_y_offset+280),
                (global_x_offset+6080,global_y_offset+280),
                (global_x_offset+7280,global_y_offset+280),
                ],entities)
            
            lootbox_taco.draw([
                (global_x_offset+3600,global_y_offset+280),
            ],entities)
            
            well.draw([
                (global_x_offset+1040,global_y_offset+440),
                (global_x_offset+1040,global_y_offset+360),
                (global_x_offset+1040,global_y_offset+280),
                (global_x_offset+2000,global_y_offset+440),
                (global_x_offset+2000,global_y_offset+360),
                (global_x_offset+2000,global_y_offset+280),
                (global_x_offset+6400,global_y_offset+440),
                (global_x_offset+7120,global_y_offset+440),
                (global_x_offset+7120,global_y_offset+360),
                (global_x_offset+7120,global_y_offset+280),
                (global_x_offset+7120,global_y_offset+200),
            ],entities)
            
            canopy.draw([
                (global_x_offset+1040,global_y_offset+120),
                (global_x_offset+2000,global_y_offset+120),
                (global_x_offset+6400,global_y_offset+280),
                (global_x_offset+7120,global_y_offset+40),
            ],entities)
            if touch == False:
                player.on_ground = False
   
    #pelaajan polo animaatio framejen tuonti
    polo_frames = []
    for i in range(1, 9):
        frame = pygame.image.load(f'Polo/Polo{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        polo_frames.append(frame)
    #pelaajan polo animaatio framejen tuonti
    marko_frames = []
    for i in range(1, 9):
        frame = pygame.image.load(f'marko/marko{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        marko_frames.append(frame)
    #koiruli framet
    doge_frames = []
    for i in range(1, 3):
        frame = pygame.image.load(f'doge/doge{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        doge_frames.append(frame)
    #auton framet
    car_frames = []
    for i in range(1, 7):
        frame = pygame.image.load(f'car/car{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        car_frames.append(frame)
        # live counter

    if lives <= 0:
        run = False
        is_running = False
        score = int(current_level_score+score)
    else:
        #juttu hyppelyyn
        touch = False

        #pelin ajamiseen tarvittava muuttuja
        run = True

        # voittiko pelaaja
        win = False
        #kello tarvitaan kaikeen
        clock = pygame.time.Clock()

        # asioiden lokaatiot suhteessa kameran 0 kohtaan
        global_x_offset = int(0)

        # asioiden lokaatiot suhteessa kameran 0 kohtaa
        global_y_offset = int()

        # nykyisen tason score
        current_level_score = 0

        #kitka
        x_delta = 1.1
        #putoamis nopeus pixeliä framessa
        y_delta = 1.1

        #testbg
        test_bg = pygame.transform.scale(pygame.image.load('materials/background_test.png'), (8000, 600))
        #level 1
        if level == 1:
            #musiikki
            pygame.mixer.music.load("sound/background_music.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =polo_frames,x_pos=0,y_pos=440,hiding=False,can_climb=False,can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x.png").convert_alpha())
            sand = Object(width=80,height=80,texture=pygame.image.load("materials/sand.png").convert_alpha())
            brick = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha())
            brick3x = Object(width=240,height=80,texture=pygame.image.load("materials/brick3x.png").convert_alpha())
            lootbox_taco = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha(),loot="taco")
            well = Object(width=160,height=80,texture=pygame.image.load("materials/well.png").convert_alpha())
            canopy = Object(width=160,height=160,texture=pygame.image.load("materials/canopy.png").convert_alpha(),can_walk_through=True)


            bg = pygame.image.load('materials/background.png')
            bg = pygame.transform.scale(bg, (8000, 600))

            food = 3000
            entities = [
                Enemy(x_pos=720,y_pos=440,x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=640,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=800,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=2000,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=2080,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=2160,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=3440,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=5360,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=4560,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car")
                        ]
            items = [
                Item(type="bucket",x_pos=7600,y_pos=440)
            ]
        elif level == 2:
            #musiikki
            pygame.mixer.music.load("sound/background_music_night.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =marko_frames,x_pos=0,y_pos=440,hiding=False,can_climb=False,can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x_night.png").convert_alpha())
            sand = Object(width=80,height=80,texture=pygame.image.load("materials/sand_night.png").convert_alpha())
            brick = Object(width=80,height=80,texture=pygame.image.load("materials/brick_night.png").convert_alpha())
            brick3x = Object(width=240,height=80,texture=pygame.image.load("materials/brick3x_night.png").convert_alpha())
            lootbox_taco = Object(width=80,height=80,texture=pygame.image.load("materials/brick_night.png").convert_alpha(),loot="sauce")
            lootbox_taco1 = Object(width=80,height=80,texture=pygame.image.load("materials/brick_night.png").convert_alpha(),loot="taco")
            well = Object(width=160,height=80,texture=pygame.image.load("materials/well_night.png").convert_alpha())
            canopy = Object(width=160,height=160,texture=pygame.image.load("materials/canopy_night.png").convert_alpha(),can_walk_through=True)

            bg = pygame.image.load('materials/background_night.png')
            bg = pygame.transform.scale(bg, (8000, 600))

            food = 3000.0
            entities = [
                Enemy(x_pos=100,y_pos=440,x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=200,y_pos=440,x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=7500,y_pos=400,x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=2400,y_pos=40,x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="car"),
                Enemy(x_pos=4000,y_pos=40,x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=5000,y_pos=40,x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),

                    ]
            items = [
                Item(type="bucket",x_pos=7360, y_pos=-40),
                Item(type="sauce",x_pos=4640, y_pos=200)
                    ]
        elif level == 3:
            #musiikki
            pygame.mixer.music.load("sound/background_music.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =polo_frames,x_pos=0,y_pos=440,hiding=False,can_climb=False,can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x_snow.png").convert_alpha())
            sand = Object(width=80,height=80,texture=pygame.image.load("materials/sand_snow.png").convert_alpha())
            brick = Object(width=80,height=80,texture=pygame.image.load("materials/brick_snow.png").convert_alpha())
            brick3x = Object(width=240,height=80,texture=pygame.image.load("materials/brick3x_snow.png").convert_alpha())
            lootbox_taco = Object(width=80,height=80,texture=pygame.image.load("materials/brick_snow.png").convert_alpha(),loot="taco")
            lootbox_taco1 = Object(width=80,height=80,texture=pygame.image.load("materials/brick_snow.png").convert_alpha(),loot="taco")
            well = Object(width=160,height=80,texture=pygame.image.load("materials/well.png").convert_alpha())
            canopy = Object(width=160,height=160,texture=pygame.image.load("materials/canopy_snow.png").convert_alpha(),can_walk_through=True)

            bg = pygame.image.load('materials/background_snow.png')
            bg = pygame.transform.scale(bg, (8000, 600))

            food = 3000.0
            entities = [
                Enemy(x_pos=600,y_pos=400,x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=650,y_pos=400,x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=700,y_pos=400,x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=800,y_pos=400,x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=2000,y_pos=400,x_velocity=2,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=4320,y_pos=360,x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=4400,y_pos=360,x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=4480,y_pos=360,x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=4560,y_pos=360,x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=6400,y_pos=200,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=6800,y_pos=200,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                    ]
            items = [
                Item(type="bucket",x_pos=7600,y_pos=440),
                Item(type="taco",x_pos=4160,y_pos=-200)
                    ]
        elif level == 4:
            #musiikki
            pygame.mixer.music.load("sound/background_music_night.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =marko_frames,x_pos=0,y_pos=440,hiding=False,can_climb=False,can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x_snow_night.png").convert_alpha())
            sand = Object(width=80,height=80,texture=pygame.image.load("materials/sand_snow_night.png").convert_alpha())
            brick = Object(width=80,height=80,texture=pygame.image.load("materials/brick_snow_night.png").convert_alpha())
            brick3x = Object(width=240,height=80,texture=pygame.image.load("materials/brick3x_snow_night.png").convert_alpha())
            lootbox_taco = Object(width=80,height=80,texture=pygame.image.load("materials/brick_snow_night.png").convert_alpha(),loot="taco")
            lootbox_taco1 = Object(width=80,height=80,texture=pygame.image.load("materials/brick_snow_night.png").convert_alpha(),loot="taco")
            well = Object(width=160,height=80,texture=pygame.image.load("materials/well_night.png").convert_alpha())
            canopy = Object(width=160,height=160,texture=pygame.image.load("materials/canopy_snow_night.png").convert_alpha(),can_walk_through=True)

            bg = pygame.image.load('materials/background_snow_night.png')
            bg = pygame.transform.scale(bg, (8000, 600))

            food = 3000.0
            entities = [
            Enemy(x_pos=400,y_pos=400,x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
            Enemy(x_pos=880,y_pos=400,x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
            Enemy(x_pos=1520,y_pos=400,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
            Enemy(x_pos=4640,y_pos=400,x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
            Enemy(x_pos=4800,y_pos=400,x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
            Enemy(x_pos=7760,y_pos=400,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                ]
            items = [
                Item(type="bucket",x_pos=7600,y_pos=-40)
                    ]
            
        if level >= 5:
            run = False
            prison = pygame.transform.scale(pygame.image.load('materials/background_prison.png').convert_alpha(), (800, 600))
            bliss = pygame.transform.scale(pygame.image.load('materials/background_bliss.png').convert_alpha(), (800, 600))
            policer = pygame.transform.scale(pygame.image.load('police/policer.png').convert_alpha(), (80, 80))
            if marko_murderer and polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(80,500))
                    screen.blit(policer,(200,500))
                    screen.blit(policer,(300,500))
                    screen.blit(polo_frames[4],(500,500))
                    screen.blit(marko_frames[4],(480,480))
                    pygame.display.update()
                    clock.tick(60)
            elif marko_murderer and not polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(80,500))
                    screen.blit(policer,(200,500))
                    screen.blit(policer,(300,500))
                    screen.blit(marko_frames[4],(500,500))
                    pygame.display.update()
                    clock.tick(60)
            elif not marko_murderer and polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(80,500))
                    screen.blit(policer,(200,500))
                    screen.blit(policer,(300,500))
                    screen.blit(polo_frames[4],(500,500))
                    pygame.display.update()
                    clock.tick(60)
            elif not marko_murderer and not polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    screen.blit(bliss,(0,0))
                    screen.blit(marko_frames[4],(140,240))
                    screen.blit(polo_frames[0],(500,500))
                    pygame.display.update()
                    clock.tick(60)
            is_running = False
            lives = 0
    while run:
        if player.hiding == True:
            food -= 0.5
        else:
            food -= 1
        #näytön tyhjennys
        screen.fill((0,0,0))

            #level 1 tausta
        if level == 1:
            screen.fill((105,192,186))
            screen.blit(bg, (global_x_offset,global_y_offset))
            if global_x_offset <= -7200:
                global_x_offset = -7200
            

                
        elif level == 2:
            screen.fill((20,30,44))
            screen.blit(bg, (global_x_offset,global_y_offset))
            if global_x_offset <= -7200:
                global_x_offset = -7200
        elif level == 3:
            screen.fill((159,230,247))
            screen.blit(bg, (global_x_offset,global_y_offset))
            if global_x_offset <= -7200:
                global_x_offset = -7200
        elif level == 4:
            screen.fill((10,17,27))
            screen.blit(bg, (global_x_offset,global_y_offset))
            if global_x_offset <= -7200:
                global_x_offset = -7200
        #screen.blit(test_bg, (global_x_offset,global_y_offset))


        #pelaajan fysiikat ja kamera
        player.update_velocity(x_delta,y_delta)

        #drawer pirtää ja testaa törmäykset pelaajan kanssa
        drawer(level,entities,items)
        #kameran liikket
        
        player.camera()

        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää 
        player.movement()

        
        if not player.alive:
            lives -= 1
            run = False
            player.x_velocity = 0
            player.y_velocity = 0
            if level == 1 or level == 3:
                pygame.mixer.music.load("sound/deadin1.wav")
            elif level == 2 or level == 4:
                pygame.mixer.music.load("sound/deadin2.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)
            for i in range(120):
                screen.fill((0,0,0))
                screen.blit(bg, (global_x_offset,global_y_offset))
                player.y_pos += player.y_velocity
                drawer(level,entities,items)
                if i < 20:
                    player.y_velocity = -10
                else:
                    player.y_velocity += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                        
                    
                screen.blit(player.character[6],(player.x_pos,player.y_pos))
                pygame.display.update()
                clock.tick(60)
            
        if win:  
            if player.character == polo_frames and has_killed:
                polo_murderer = True
            elif player.character == marko_frames and has_killed:
                marko_murderer = True

            current_level_score += food//10*10
            score += current_level_score
            pygame.mixer.music.load("sound/winnin.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)
            flippera = False
            flipperb = False                            

            run = False
            
            for i in range(30):
                #ikkunan sulkeminen
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                screen.fill((0,0,0))
                screen.blit(bg, (global_x_offset,global_y_offset))
                screen.blit(pygame.transform.flip(player.character[0],flippera,flipperb),(player.x_pos,player.y_pos))
                drawer(level,entities,items)
                if flippera == False and flipperb == True:
                    flipperb = False            
                elif flippera == True and flipperb == True:
                    flippera = False
                elif flippera == True and flipperb == True:
                    flipperb = True
                elif flippera == True and flipperb == False:
                    flipperb = True
                elif flippera == False and flipperb == False:
                    flippera = True


                
                
                
                
                pygame.display.update()                                       
                clock.tick(15)
            level += 1
        #ikkunan sulkeminen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        #pelaajan kuolema pudotukseen
        if ((player.y_pos > 700+global_y_offset) and (player.alive) or food <= 0):
            lives -= 1
            run = False
            if level == 1 or level == 3:
                pygame.mixer.music.load("sound/deadin1.wav")
            elif level == 2 or level == 4:
                pygame.mixer.music.load("sound/deadin2.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)
            for i in range(120):
                screen.fill((0,0,0))
                screen.blit(bg, (global_x_offset,global_y_offset))
                player.update_velocity(x_delta,y_delta)
                drawer(level,entities,items)
                
                
                screen.blit(player.character[4],(player.x_pos,player.y_pos))
                pygame.display.update()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
        #hud
        if level % 2 == 0:
            screen.blit(font.render("lives",False,(255,255,255)),(650,0))
            screen.blit(font.render(f"{lives}",False,(255,255,255)),(700,50))
            screen.blit(font.render("food",False,(255,255,255)),(250,0))
            screen.blit(font.render(f"{int(food//10)}",False,(255,255,255)),(300,50))
            screen.blit(font.render("level",False,(255,255,255)),(450,0))
            screen.blit(font.render(f"{level}",False,(255,255,255)),(500,50))
            screen.blit(font.render("score",False,(255,255,255)),(50,0))
            screen.blit(font.render(f"{int(score+current_level_score)}",False,(255,255,255)),(100,50))
        else:
            screen.blit(font.render("lives",False,(0,0,0)),(650,0))
            screen.blit(font.render(f"{lives}",False,(0,0,0)),(700,50))
            screen.blit(font.render("food",False,(0,0,0)),(250,0))
            screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(300,50))
            screen.blit(font.render("level",False,(0,0,0)),(450,0))
            screen.blit(font.render(f"{level}",False,(0,0,0)),(500,50))
            screen.blit(font.render("score",False,(0,0,0)),(50,0))
            screen.blit(font.render(f"{int(score+current_level_score)}",False,(0,0,0)),(100,50))
 
        #näytön päyivitys
        pygame.display.update()

        #suorituksen nopeus
        clock.tick(60)
if lives <= 0:
    #musiikki
    pygame.mixer.music.load("sound/background_music_best.wav")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    screen.fill((0,0,0))
    screen.blit(fontxl.render('GAME OVER',False,(255,255,255)),(80,250))
    pygame.display.update()
    pygame.time.delay(1000)
    ask = True
    writing = False
    yes = False
    while ask:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    writing = True
                    ask = False
                elif event.key == pygame.K_ESCAPE:
                    writing = False
                    ask = False
                    yes = True
        screen.fill((0,0,0))
        screen.blit(font.render('press enter to save score',False,(255,255,255)),(80,250))
        screen.blit(font.render('press esc to continue without saving',False,(255,255,255)),(80,280))
        pygame.display.update()
        clock.tick(60)
    name = ""
    while writing: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    writing = False
                    yes = True
                    save_this =[]
                    with open("SuperMarkoBrothers.csv", "r") as file:
                        
                        csvreader = csv.reader(file)
                        for indexi,row in enumerate(csvreader):
                            if len(row)>= 0:
                                if score > int(row[1]) and not [name,score] in save_this:
                                    save_this.append([name,score])
                                save_this.append(row)
                            
                        if not [name,score] in save_this:
                            save_this.append([name,score])
                                
                    with open("SuperMarkoBrothers.csv", "w", newline='') as file:
                        file.truncate()
                        writer = csv.writer(file)
                        writer.writerows(save_this) 
                        
                elif len(name) < 8 and not event.key == pygame.K_TAB:
                    name += event.unicode
        screen.fill((0,0,0))
        screen.blit(font.render("Enter Your Name Below. max 8 characters.",False,(255,255,255)),(0,0))
        screen.blit(font.render("(press esc to stop)",False,(255,255,255)),(0,30))
        screen.blit(fontxl.render(name,False,(255,255,255)),(80,250))
        pygame.display.update()
    high_scores = []
    with open("SuperMarkoBrothers.csv", "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            high_scores.append(row)
    while len(high_scores) < 12:
        high_scores.append(["",""])
    scroll = 0
    while yes:
        screen.fill((0,0,0))
        screen.blit(font.render(f"{1+scroll}",False,(255,255,255)),(0,0))
        screen.blit(font.render(high_scores[scroll+0][0],False,(255,255,255)),(100,0))
        screen.blit(font.render(high_scores[scroll+0][1],False,(255,255,255)),(400,0))
        screen.blit(font.render(f"{2+scroll}",False,(255,255,255)),(0,50))
        screen.blit(font.render(high_scores[scroll+1][0],False,(255,255,255)),(100,50))
        screen.blit(font.render(high_scores[scroll+1][1],False,(255,255,255)),(400,50))
        screen.blit(font.render(f"{3+scroll}",False,(255,255,255)),(0,100))
        screen.blit(font.render(high_scores[scroll+2][0],False,(255,255,255)),(100,100))
        screen.blit(font.render(high_scores[scroll+2][1],False,(255,255,255)),(400,100))
        screen.blit(font.render(f"{4+scroll}",False,(255,255,255)),(0,150))
        screen.blit(font.render(high_scores[scroll+3][0],False,(255,255,255)),(100,150))
        screen.blit(font.render(high_scores[scroll+3][1],False,(255,255,255)),(400,150))
        screen.blit(font.render(f"{5+scroll}",False,(255,255,255)),(0,200))
        screen.blit(font.render(high_scores[scroll+4][0],False,(255,255,255)),(100,200))
        screen.blit(font.render(high_scores[scroll+4][1],False,(255,255,255)),(400,200))
        screen.blit(font.render(f"{6+scroll}",False,(255,255,255)),(0,250))
        screen.blit(font.render(high_scores[scroll+5][0],False,(255,255,255)),(100,250))
        screen.blit(font.render(high_scores[scroll+5][1],False,(255,255,255)),(400,250))
        screen.blit(font.render(f"{7+scroll}",False,(255,255,255)),(0,300))
        screen.blit(font.render(high_scores[scroll+6][0],False,(255,255,255)),(100,300))
        screen.blit(font.render(high_scores[scroll+6][1],False,(255,255,255)),(400,300))
        screen.blit(font.render(f"{8+scroll}",False,(255,255,255)),(0,350))
        screen.blit(font.render(high_scores[scroll+7][0],False,(255,255,255)),(100,350))
        screen.blit(font.render(high_scores[scroll+7][1],False,(255,255,255)),(400,350))
        screen.blit(font.render(f"{9+scroll}",False,(255,255,255)),(0,400))
        screen.blit(font.render(high_scores[scroll+8][0],False,(255,255,255)),(100,400))
        screen.blit(font.render(high_scores[scroll+8][1],False,(255,255,255)),(400,400))
        screen.blit(font.render(f"{10+scroll}",False,(255,255,255)),(0,450))
        screen.blit(font.render(high_scores[scroll+9][0],False,(255,255,255)),(100,450))
        screen.blit(font.render(high_scores[scroll+9][1],False,(255,255,255)),(400,450))
        screen.blit(font.render(f"{11+scroll}",False,(255,255,255)),(0,500))
        screen.blit(font.render(high_scores[scroll+10][0],False,(255,255,255)),(100,500))
        screen.blit(font.render(high_scores[scroll+10][1],False,(255,255,255)),(400,500))
        screen.blit(font.render(f"{12+scroll}",False,(255,255,255)),(0,550))
        screen.blit(font.render(high_scores[scroll+11][0],False,(255,255,255)),(100,550))
        screen.blit(font.render(high_scores[scroll+11][1],False,(255,255,255)),(400,550))
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if scroll+12 < len(high_scores):
                        scroll += 1
                if event.key == pygame.K_UP:
                    if scroll > 0:
                        scroll -= 1
                if event.key == pygame.K_ESCAPE:
                    yes = False
#sulkee pygamen
pygame.quit()
