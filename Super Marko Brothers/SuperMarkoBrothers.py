#the code goes here

# Super Marko Brothers
# the original game with the original name
# and the defenitely original code
# and some of the code wasent from stackoverflow
# true story
# i saw it on my own eyes
# so you can trust me
# frfr
# i would never lie to you
# i am a trustworthy person
# i am not a liar

import pygame, csv, ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screensize2 = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
#screensize = (800, 600)

if screensize[0] / 10 < screensize[1] / 7.5:
    size = screensize[0] // 10
    print("1")
else:
    size = screensize[1] // 7.5
    print("2")
print(size)
#dsize = 100
print(size)
print(screensize)
#pygamen initialisaatio
pygame.init()
pygame.mixer.init()
is_running = True
lives = 3
level = 1
score = 0
polo_murderer = False
marko_murderer = False
f11_timeout = True
#size = 80
t_velocity = 9

#näytön asetuksia

SCREEN_WIDTH = size*10
SCREEN_HEIGHT = size*7.5
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)

windowsize = pygame.display.get_window_size()
print(windowsize)
#ikkunan nimi
pygame.display.set_caption("Super Marko Brothers")
#ikkunan kuvake
pygame.display.set_icon(pygame.image.load('Smb_ico.png'))
#fontti
font =pygame.font.Font('freesansbold.ttf', 32)
fontxl =pygame.font.Font('freesansbold.ttf', 100)


jump_sound = pygame.mixer.Sound("sound/jump.wav")
jump_sound.set_volume(0.01)
taco_sound = pygame.mixer.Sound("sound/taco_sound.wav")
taco_sound.set_volume(0.01)
while is_running:
    has_killed = False
    #pelin elollisten olijoiden attributejen tallennukseen käytettävä classi
    class Attribute:
        def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float,character, x_pos:float, y_pos:float, can_jump:bool, jump_time:int, jump:int, max_jump:int):
            self.y_velocity = y_velocity #tämän hetkinen nopeus
            self.x_velocity = x_velocity #tämän hetkinen nopeus
            self.on_ground = on_ground #onko pelaaja maassa
            self.speed = speed *(size/80)# mikä on pelaajan kiihtyvyys
            self.character = character #onko pelaaja polo vai marko
            self.x_pos = x_pos #pelaajan lokaatio
            self.y_pos = y_pos #pelaajan lokaatio
            self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,size,size) #pelaajan hitbox
            self.can_jump = can_jump #voiko pelaaja hyppiä
            self.jump_time = jump_time #kuinks pitkään pelaaja on hypännyt
            self.jump = jump * (size/80) #pelaajan hyppy voima
            self.max_jump = max_jump #aika hz
            self.alive = True #onko pelaaja hengissä
            self.frameid = 0 #pelaajan tämän hetkinen animaatio kehys
            self.delay = 0 #animaation kehysten välinen viive tällä hetkellä
            self.frame_count = 4 #kuinka monta kehystä animaatiossa on (kävely ei muut)

        def update_velocity(self, x_delta, gravity):
            if self.y_velocity > t_velocity*(size/80):
                self.y_velocity = t_velocity*(size/80)
            else:
                self.y_velocity += gravity
            self.x_velocity = self.x_velocity * x_delta 
            
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            
            self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,size,size)

            


        def camera(self):
            global global_x_offset
            global global_y_offset
            
            if self.x_pos >= 400*(size/80):
                self.x_pos = (400*(size/80))-1
                if self.x_velocity > 0:
                    global_x_offset -= self.x_velocity
                else:
                    global_x_offset += self.x_velocity
            if self.y_pos <= 50*(size/80):
                self.y_pos = (50*(size/80))-1
                global_y_offset -= self.y_velocity
            if (self.y_pos >= 50*(size/80)) and (not global_y_offset < 1*(size/80)):
                self.y_pos = 50*(size/80)
                global_y_offset -= self.y_velocity
            if global_y_offset <= 0:
                global_y_offset = 0
            if self.x_pos <= 0:
                self.x_pos = 0
                self.x_velocity = 0                                   
            if self.x_pos >= size*10:
                self.x_pos = (size*10)-1
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
                print((self.x_pos-global_x_offset)//size*size,(self.y_pos-global_y_offset)//size*size+(size/2))
            if self.on_ground:
                self.can_jump = True
                self.jump_time = 0
            elif 0 < self.jump_time < self.max_jump:
                self.can_jump = True
            else:
                self.on_ground = False
                self.can_jump = False
                

            #hyppiminen
            if (key[pygame.K_w] == True) and (self.can_jump == True):
                self.y_velocity = self.jump
                self.jump_time += 1
                jump_sound.play()
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
            #kävely
            elif (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
                screen.blit(self.character[0],(self.x_pos,self.y_pos))
            elif key[pygame.K_a] == True:
                self.x_velocity += -self.speed
                screen.blit(pygame.transform.flip(self.character[self.frameid],True,False),(self.x_pos,self.y_pos))
            elif key[pygame.K_d] == True:
                self.x_velocity += self.speed
                screen.blit(self.character[self.frameid],(self.x_pos,self.y_pos))
            else:
                screen.blit(self.character[0],(self.x_pos,self.y_pos))

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
                        if (location[1] < player.y_pos + size < location[1] +(size/4)) and (location[0]-size+(size/8) < player.x_pos < location[0]+self.width-(size/8)):
                            player.y_pos = location[1] - self.height
                            player.y_velocity = 0
                            player.on_ground = True
                            touch = True

                        #osumat palikan alla
                        if (location[1] +self.height >= player.y_pos >= location[1] +self.height -(size/4)) and (location[0]-size+(size/8) <= player.x_pos <= location[0]+self.width-(size/8)):
                            player.y_pos = location[1] +self.height
                            if not self.loot == None:
                                items.append(Item(type=f"{self.loot}",x_pos=location[0]-global_x_offset,y_pos=location[1]-size-global_y_offset))
                                self.loot = None

                        #osumat palikan vasen laita
                        if (location[0] <= player.x_pos+size <= location[0] +(size/4)) and (location[1]+(size/8) <= player.y_pos +size <= location[1]+self.height+size-(size/8)):
                            player.x_pos = location[0] -size

                        #osumat palikan oikea laita
                        if (location[0] + self.width >= player.x_pos >= location[0]-(size/4)) and (location[1]+(size/8) <= player.y_pos +size <= location[1]+self.height+size-(size/8)):
                            player.x_pos = location[0] +self.width

                if not entities == None:
                #npc osumat        
                    for entity in entities:
                        for location in lista:
                            #osumat palikan päällä
                            if (location[1] < entity.y_pos + size+global_y_offset < location[1] +(size/4)) and (location[0]-size < entity.x_pos + global_x_offset < location[0]+self.width):
                                entity.y_pos = location[1] - self.height -global_y_offset
                                entity.y_velocity = 0


                            #osumat palikan alla
                            if (location[1] +self.height >= entity.y_pos+global_y_offset >= location[1] +self.height -(size/4)) and (location[0]-size <= entity.x_pos + global_x_offset <= location[0]+self.width):
                                entity.y_pos = location[1] +self.height -global_y_offset

                            #osumat palikan vasen laita
                            if (location[0] <= entity.x_pos + global_x_offset+size <= location[0] +(size/4)) and (location[1]+(size/8) <= entity.y_pos+global_y_offset +size <= location[1]+self.height+size-(size/8)):
                                entity.x_pos = location[0] -size -global_x_offset
                                if entity.x_velocity > 0:
                                    entity.x_velocity = -entity.x_velocity
                                
                            #osumat palikan oikea laita
                            if (location[0] + self.width >= entity.x_pos + global_x_offset >= location[0]-(size/4)) and (location[1]+(size/8) <= entity.y_pos+global_y_offset +size <= location[1]+self.height+size-(size/8)):
                                entity.x_pos = location[0] +self.width - global_x_offset
                                if entity.x_velocity < 0:
                                    entity.x_velocity = -entity.x_velocity
                               
    class Enemy:        
        def __init__(self, y_velocity:float, x_velocity:float,x_pos:int,y_pos:int, frame_count:int, anim_speed:int, type:str):
            self.y_velocity = y_velocity
            self.x_velocity = x_velocity * (size/80)
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.frameid = 0
            self.delay = 0
            self.anim_speed = anim_speed
            self.frame_count = frame_count
            self.character = eval(f"{type}_frames")
            self.rect = pygame.rect.Rect(self.x_pos+(size/8)+global_x_offset,self.y_pos+global_y_offset+(size/8),(size*0.75),(size*0.75))
            self.type = type
            self.flip = False
        def update(self,gravity:float):
            if self.y_velocity > t_velocity*(size/80):
                self.y_velocity = t_velocity*(size/80)
            else:
                self.y_velocity += gravity*(size/80)
            
            
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            
            self.rect = pygame.rect.Rect(self.x_pos+(size/8)+global_x_offset,self.y_pos+global_y_offset+(size/8),(size*0.75),(size*0.75))
            
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
            self.texture = pygame.transform.scale(pygame.image.load(f'items/{type}.png').convert_alpha(),(size,size))
            self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,size,size)
        
        def draw(self):
            screen.blit(self.texture,(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
            self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,size,size)


    def drawer(level:int,entities:list,items:list):
        global lives
        global run
        global current_level_score
        global win
        global food
        global has_killed
        global touch

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
                    lives += 1
                elif item.type == "sauce":
                    lives += 1
        for take in collect:
            items.remove(take)
        for item in items:
            if (item.x_pos <= -global_x_offset + (size*10)):
                item.draw()
                




        ded = []
        # npc kuolemat ja tapot
        for entity in entities:
            if entity.y_pos >= (size*8.75):
                ded.append(entity)


            if entity.type == "doge":
                if (entity.x_pos + global_x_offset+(size/16) <= player.x_pos+size <= entity.x_pos +(size*2)+ global_x_offset-(size/16)) and (entity.y_pos+global_y_offset-size-(size/4) <= player.y_pos <= entity.y_pos+global_y_offset-size) and (player.y_velocity > 0): 
                    ded.append(entity)
                    player.y_velocity = player.jump
                    current_level_score += 100
                    has_killed = True
                elif pygame.Rect.colliderect(entity.rect,player.rect):
                    
                    player.alive = False 


            elif entity.type == "car":
                if (entity.x_pos + global_x_offset+(size/8) <= player.x_pos+size <= entity.x_pos +(size*2)+ global_x_offset-(size/8)) and (entity.y_pos+global_y_offset-size-(size/4) <= player.y_pos <= entity.y_pos+global_y_offset-size) and (player.y_velocity > 0): 
                    player.y_velocity = player.jump
                    if entity.flip == False:
                        entity.flip = True
                        current_level_score += 100
                        entity.x_velocity = entity.x_velocity * 10
                    else:
                        entity.x_velocity = -entity.x_velocity
                    has_killed = True
                elif pygame.Rect.colliderect(entity.rect,player.rect) and player.alive:
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
                    if (i.y_pos + global_y_offset < entity.y_pos + size < i.y_pos + global_y_offset +(size/4)) and (i.x_pos + global_x_offset-size < entity.x_pos + global_x_offset < i.x_pos + global_x_offset+size):
                        entity.y_pos = i.y_pos -size
                        entity.y_velocity = 0
                    #osumat olion alla
                    if (i.y_pos+ global_y_offset +size >= entity.y_pos >= i.y_pos+ global_y_offset +size -(size/4)) and (i.x_pos + global_x_offset-size <= entity.x_pos + global_x_offset <= i.x_pos + global_x_offset+size):
                        entity.y_pos = i.y_pos +size

                    #osumat olion vasen laita
                    if (i.x_pos+ + global_x_offset <= entity.x_pos + global_x_offset+size <= i.x_pos + global_x_offset +(size/4)) and (i.y_pos+(size/8)+global_y_offset <= entity.y_pos +size <= i.y_pos+size+size-(size/8)+global_y_offset):
                        entity.x_pos = i.x_pos -size 
                        if entity.x_velocity > 0:
                            entity.x_velocity = -entity.x_velocity

                    #osumat polion oikea laita
                    if (i.x_pos + global_x_offset + size >= entity.x_pos + global_x_offset >= i.x_pos + global_x_offset-(size/4)) and (i.y_pos+(size/8)+global_y_offset <= entity.y_pos +size <= i.y_pos+size+size-(size/8)+global_y_offset):
                        entity.x_pos = i.x_pos +size
                        if entity.x_velocity < 0:
                            entity.x_velocity = -entity.x_velocity
        for bury in ded:
            entities.remove(bury)
        for entity in entities:
            if not entity.x_pos >= -global_x_offset + (size*12.5):
                entity.update(gravity)

        if level == 1:
            
            touch = False

            sand10x.draw([
                (global_x_offset,global_y_offset+(size*6.5)),
                (global_x_offset+(size*10),global_y_offset+(size*6.5)),
                (global_x_offset+(size*23),global_y_offset+(size*6.5)),
                (global_x_offset+(size*36),global_y_offset+(size*6.5)),
                (global_x_offset+(size*50),global_y_offset+(size*6.5)),
                (global_x_offset+(size*60),global_y_offset+(size*6.5)),
                (global_x_offset+(size*90),global_y_offset+(size*6.5))
                ],entities)
            
            sand.draw([
                (global_x_offset+(size*74),global_y_offset+(size*6.5)),
                (global_x_offset+(size*81),global_y_offset+(size*6.5))
                ],entities)
            
            brick3x.draw([
                (global_x_offset+(size*83),global_y_offset+(size*3.5)),
                (global_x_offset+(size*57),global_y_offset+(size*3.5))
                ],entities)
            
            brick.draw([
                (global_x_offset+(size*31),global_y_offset+(size*5.5)),
                (global_x_offset+(size*32),global_y_offset+(size*5.5)),
                (global_x_offset+(size*32),global_y_offset+(size*4.5)),
                (global_x_offset+(size*76),global_y_offset+(size*3.5))
                ],entities)
            lootbox_taco.draw([
                (global_x_offset+(size*4),global_y_offset+(size*3.5))
            ],entities)
            well.draw([
                (global_x_offset+(size*10),global_y_offset+(size*5.5)),
                (global_x_offset+(size*18),global_y_offset+(size*5.5)),
                (global_x_offset+(size*18),global_y_offset+(size*4.5)),
                (global_x_offset+(size*18),global_y_offset+(size*3.5)),
                (global_x_offset+(size*23),global_y_offset+(size*5.5)),
                (global_x_offset+(size*23),global_y_offset+(size*4.5)),
                (global_x_offset+(size*23),global_y_offset+(size*3.5)),
                (global_x_offset+(size*44),global_y_offset+(size*5.5))
            ],entities)
            canopy.draw([
                (global_x_offset+(size*10),global_y_offset+(size*3.5)),
                (global_x_offset+(size*18),global_y_offset+(size*1.5)),
                (global_x_offset+(size*23),global_y_offset+(size*1.5)),
                (global_x_offset+(size*44),global_y_offset+(size*3.5))
            ],entities)
            if touch == False:
                player.on_ground = False
        elif level == 2:
            touch = False

            sand10x.draw([
                (global_x_offset,global_y_offset+(size*6.5)),
                (global_x_offset+(size*10),global_y_offset+(size*6.5)),
                (global_x_offset+(size*23),global_y_offset+(size*6.5)),
                (global_x_offset+(size*36),global_y_offset+(size*6.5)),
                (global_x_offset+(size*50),global_y_offset+(size*6.5)),
                (global_x_offset+(size*60),global_y_offset+(size*6.5)),
                (global_x_offset+(size*90),global_y_offset+(size*6.5))
                ],entities)
            
            sand.draw([
                (global_x_offset+(size*74),global_y_offset+(size*6.5)),
                (global_x_offset+(size*81),global_y_offset+(size*6.5)),
                (global_x_offset+(size*20),global_y_offset+(size*6.5)),
                (global_x_offset+(size*21),global_y_offset+(size*6.5)),
                (global_x_offset+(size*22),global_y_offset+(size*6.5))
                
                ],entities)
            
            brick3x.draw([
                (global_x_offset+(size*20),global_y_offset+(size*5.5)),
                (global_x_offset+(size*83),global_y_offset+(size*3.5)),
                (global_x_offset+(size*91),global_y_offset+(size*0.5)),
                (global_x_offset+(size*57),global_y_offset+(size*3.5))
                
                ],entities)
            
            brick.draw([
                (global_x_offset+(size*33),global_y_offset+(size*6.5)),
                (global_x_offset+(size*76),global_y_offset+(size*3.5)),
                (global_x_offset+(size*99),global_y_offset+(size*5.5)),
                (global_x_offset+(size*99),global_y_offset+(size*6.5)),
                (global_x_offset+(size*99),global_y_offset+(size*4.5)),
                (global_x_offset+(size*99),global_y_offset+(size*3.5)),
                (global_x_offset+(size*96),global_y_offset+(size*2.5)),
                (global_x_offset+(size*97),global_y_offset+(size*2.5)),
                (global_x_offset+(size*94),global_y_offset+(size*3.5))
                
                ],entities)
            
            lootbox_taco.draw([
                (global_x_offset+(size*88),global_y_offset+(size*3.5))
            ])
            lootbox_taco1.draw([
                (global_x_offset+(size*95),global_y_offset+(size*2.5))
            ])

            well.draw ([
                (global_x_offset+(size*32),global_y_offset+(size*5.5))
            ],entities)
            canopy.draw ([
                (global_x_offset+(size*32),global_y_offset+(size*3.5))
            ])
            if touch == False:
                player.on_ground = False
        elif level == 3:
            touch = False

            sand10x.draw([
                (global_x_offset,global_y_offset+(size*6.5)),
                (global_x_offset+(size*10),global_y_offset+(size*6.5)),
                (global_x_offset+(size*23),global_y_offset+(size*6.5)),
                
                (global_x_offset+(size*50),global_y_offset+(size*6.5)),
                (global_x_offset+(size*60),global_y_offset+(size*6.5)),
                (global_x_offset+(size*90),global_y_offset+(size*6.5))
                ],entities)
            
            sand.draw([
                (global_x_offset+(size*69),global_y_offset+(size*5.5)),
                (global_x_offset+(size*74),global_y_offset+(size*6.5)),
                (global_x_offset+(size*77),global_y_offset+(size*6.5)),
                (global_x_offset+(size*81),global_y_offset+(size*6.5))
                ],entities)
            
            brick3x.draw([
                (global_x_offset+(size*14),global_y_offset+(size*3.5)),
                (global_x_offset+(size*35),global_y_offset+(size*6.5)),
                (global_x_offset+(size*52),global_y_offset+(size*5.5)),
                (global_x_offset+(size*52),global_y_offset+(size*3.5)),
                (global_x_offset+(size*55),global_y_offset+(size*5.5)),
                (global_x_offset+(size*55),global_y_offset+(size*3.5)),
                (global_x_offset+(size*78),global_y_offset+(size*3.5)),
                (global_x_offset+(size*83),global_y_offset+(size*3.5))
                ],entities)
            
            brick.draw([
                (global_x_offset+(size*15),global_y_offset+(size*0.5)),
                (global_x_offset+(size*17),global_y_offset+(size*-1.5)),
                (global_x_offset+(size*31),global_y_offset+(size*5.5)),
                (global_x_offset+(size*32),global_y_offset+(size*5.5)),
                (global_x_offset+(size*32),global_y_offset+(size*4.5)),
                (global_x_offset+(size*37),global_y_offset+(size*2.5)),
                (global_x_offset+(size*38),global_y_offset+(size*2.5)),
                (global_x_offset+(size*44),global_y_offset+(size*6.5)),
                (global_x_offset+(size*45),global_y_offset+(size*6.5)),
                (global_x_offset+(size*52),global_y_offset+(size*2.5)),
                (global_x_offset+(size*52),global_y_offset+(size*1.5)),
                (global_x_offset+(size*74),global_y_offset+(size*3.5)),
                (global_x_offset+(size*75),global_y_offset+(size*3.5))
                ],entities)
            lootbox_taco.draw([
                (global_x_offset+(size*16),global_y_offset+(size*3.5))
            ],entities)
            well.draw([
                (global_x_offset+(size*10),global_y_offset+(size*5.5)),
                (global_x_offset+(size*23),global_y_offset+(size*5.5)),
                (global_x_offset+(size*23),global_y_offset+(size*4.5)),
                (global_x_offset+(size*23),global_y_offset+(size*3.5)),
                (global_x_offset+(size*23),global_y_offset+(size*2.5)),
                (global_x_offset+(size*44),global_y_offset+(size*5.5)),
                (global_x_offset+(size*54),global_y_offset+(size*2.5))
            
            ],entities)
            canopy.draw([
                (global_x_offset+(size*10),global_y_offset+(size*3.5)),
                
                (global_x_offset+(size*23),global_y_offset+(size*0.5)),
                (global_x_offset+(size*44),global_y_offset+(size*3.5)),
                (global_x_offset+(size*54),global_y_offset+(size*0.5))
            ],entities)
            if touch == False:
                player.on_ground = False
        elif level == 4:
            touch = False

            sand10x.draw([
                (global_x_offset,global_y_offset+(size*6.5)),
                (global_x_offset+(size*10),global_y_offset+(size*6.5)),
                (global_x_offset+(size*50),global_y_offset+(size*6.5)),
                (global_x_offset+(size*60),global_y_offset+(size*6.5)),
                (global_x_offset+(size*70),global_y_offset+(size*6.5)),
                (global_x_offset+(size*90),global_y_offset+(size*6.5)),
                
                ],entities)
            
            sand.draw([

                (global_x_offset+(size*24),global_y_offset+(size*6.5)),
                (global_x_offset+(size*25),global_y_offset+(size*6.5)),
                (global_x_offset+(size*26),global_y_offset+(size*6.5)),
                (global_x_offset+(size*27),global_y_offset+(size*6.5)),
                (global_x_offset+(size*28),global_y_offset+(size*6.5)),
                (global_x_offset+(size*40),global_y_offset+(size*6.5)),
                (global_x_offset+(size*41),global_y_offset+(size*6.5)),
                (global_x_offset+(size*42),global_y_offset+(size*6.5)),
                (global_x_offset+(size*43),global_y_offset+(size*6.5)),
                (global_x_offset+(size*47),global_y_offset+(size*6.5)),
                (global_x_offset+(size*80),global_y_offset+(size*6.5)),
                (global_x_offset+(size*81),global_y_offset+(size*6.5)),
                (global_x_offset+(size*89),global_y_offset+(size*6.5)),
                ],entities)
            
            brick3x.draw([
                (global_x_offset+(size*32),global_y_offset+(size*3.5)),
                (global_x_offset+(size*59),global_y_offset+(size*3.5)),
                (global_x_offset+(size*83),global_y_offset+(size*3.5)),
                (global_x_offset+(size*94),global_y_offset+(size*0.5)),
                ],entities)
            
            brick.draw([
                (global_x_offset+(size*19),global_y_offset+(size*3.5)),
                (global_x_offset+(size*76),global_y_offset+(size*3.5)),
                (global_x_offset+(size*91),global_y_offset+(size*3.5)),
                ],entities)
            
            lootbox_taco.draw([
                (global_x_offset+(size*45),global_y_offset+(size*3.5)),
            ],entities)
            
            well.draw([
                (global_x_offset+(size*13),global_y_offset+(size*5.5)),
                (global_x_offset+(size*13),global_y_offset+(size*4.5)),
                (global_x_offset+(size*13),global_y_offset+(size*3.5)),
                (global_x_offset+(size*25),global_y_offset+(size*5.5)),
                (global_x_offset+(size*25),global_y_offset+(size*4.5)),
                (global_x_offset+(size*25),global_y_offset+(size*3.5)),
                (global_x_offset+(size*80),global_y_offset+(size*5.5)),
                (global_x_offset+(size*89),global_y_offset+(size*5.5)),
                (global_x_offset+(size*89),global_y_offset+(size*4.5)),
                (global_x_offset+(size*89),global_y_offset+(size*3.5)),
                (global_x_offset+(size*89),global_y_offset+(size*2.5)),
            ],entities)
            
            canopy.draw([
                (global_x_offset+(size*13),global_y_offset+(size*1.5)),
                (global_x_offset+(size*25),global_y_offset+(size*1.5)),
                (global_x_offset+(size*80),global_y_offset+(size*3.5)),
                (global_x_offset+(size*89),global_y_offset+(size*0.5)),
            ],entities)
            if touch == False:
                player.on_ground = False
    def hud():
        #hud
        screen.blit(font.render("lives",False,(0,0,0)),(size*8.125,0))
        screen.blit(font.render(f"{lives}",False,(0,0,0)),(size*8.75,size*0.625))
        screen.blit(font.render("food",False,(0,0,0)),(size*3.125,0))
        if food//10 >= 100:
            screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(size*3.25,size*0.625))
        elif food//10 >= 10:
            screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(size*3.5,size*0.625))
        else:
            screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(size*3.75,size*0.625))

        screen.blit(font.render("level",False,(0,0,0)),(size*5.625,0))
        screen.blit(font.render(f"{level}",False,(0,0,0)),(size*6.25,size*0.625))
        screen.blit(font.render("score",False,(0,0,0)),(size*0.625,0))
        screen.blit(font.render(f"{int(score+current_level_score)}",False,(0,0,0)),(size*1.25,size*0.625))

    def score_board():
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
    def cover():
        global windowsize
        pygame.draw.rect(screen,(0,0,0),pygame.rect.Rect(size*10,0,screensize[0],screensize[1]))
        pygame.draw.rect(screen,(0,0,0),pygame.rect.Rect(0,size*7.5,screensize[0],screensize[1]))        
        windowsize = pygame.display.get_window_size()
    def fullscreen():
        global f11_timeout
        key = pygame.key.get_pressed()
        if key[pygame.K_F11] and f11_timeout:
            pygame.display.toggle_fullscreen()
            f11_timeout = False
        elif not key[pygame.K_F11] and not f11_timeout:
            f11_timeout = True

    #pelaajan polo animaatio framejen tuonti
    polo_frames = []
    for i in range(1, 8):
        frame = pygame.image.load(f'Polo/Polo{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(size,size))
        polo_frames.append(frame)
    #pelaajan polo animaatio framejen tuonti
    marko_frames = []
    for i in range(1, 8):
        frame = pygame.image.load(f'marko/marko{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(size,size))
        marko_frames.append(frame)
    #koiruli framet
    doge_frames = []
    for i in range(1, 3):
        frame = pygame.image.load(f'doge/doge{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(size,size))
        doge_frames.append(frame)
    #auton framet
    car_frames = []
    for i in range(1, 7):
        frame = pygame.image.load(f'car/car{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(size,size))
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
        global_y_offset = int(0)

        # nykyisen tason score
        current_level_score = 0

        #kitka
        x_delta = 0.91
        #putoamis nopeus pixeliä framessa (irl (40*9)/60= 6 missä 40 = 1m, 9 = painovoima, 60 = kellotaajuus. )
        gravity = 1.1*(size/80)

        #testbg
        test_bg = pygame.transform.scale(pygame.image.load('materials/background_test.png'), ((size*100), (size*7.5)))
        #level 1
        bg_colour = (0,0,0)
        if level == 1:
            #musiikki
            pygame.mixer.music.load("sound/background_music.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =polo_frames,x_pos=0,y_pos=(size*5.5),can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=(size*10),height=size,texture=pygame.image.load("materials/sand10x.png").convert_alpha())
            sand = Object(width=size,height=size,texture=pygame.image.load("materials/sand.png").convert_alpha())
            brick = Object(width=size,height=size,texture=pygame.image.load("materials/brick.png").convert_alpha())
            brick3x = Object(width=(size*3),height=size,texture=pygame.image.load("materials/brick3x.png").convert_alpha())
            lootbox_taco = Object(width=size,height=size,texture=pygame.image.load("materials/brick.png").convert_alpha(),loot="taco")
            well = Object(width=(size*2),height=size,texture=pygame.image.load("materials/well.png").convert_alpha())
            canopy = Object(width=(size*2),height=(size*2),texture=pygame.image.load("materials/canopy.png").convert_alpha(),can_walk_through=True)

            bg_colour = (105,192,186)
            bg = pygame.image.load('materials/background.png')
            bg = pygame.transform.scale(bg, ((size*100), (size*7.5)))

            food = 3000
            entities = [
                Enemy(x_pos=(size*9),y_pos=(size*5.5),x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=(size*8),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*10),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*25),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*26),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*27),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*43),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*67),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=(size*57),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car")
                        ]
            items = [
                Item(type="bucket",x_pos=(size*95),y_pos=(size*5.5))
            ]
        elif level == 2:
            #musiikki
            pygame.mixer.music.load("sound/background_music_night.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =marko_frames,x_pos=0,y_pos=(size*5.5),can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=(size*10),height=size,texture=pygame.image.load("materials/sand10x_night.png").convert_alpha())
            sand = Object(width=size,height=size,texture=pygame.image.load("materials/sand_night.png").convert_alpha())
            brick = Object(width=size,height=size,texture=pygame.image.load("materials/brick_night.png").convert_alpha())
            brick3x = Object(width=(size*3),height=size,texture=pygame.image.load("materials/brick3x_night.png").convert_alpha())
            lootbox_taco = Object(width=size,height=size,texture=pygame.image.load("materials/brick_night.png").convert_alpha(),loot="taco")
            lootbox_taco1 = Object(width=size,height=size,texture=pygame.image.load("materials/brick_night.png").convert_alpha(),loot="taco")
            well = Object(width=(size*2),height=size,texture=pygame.image.load("materials/well_night.png").convert_alpha())
            canopy = Object(width=(size*2),height=(size*2),texture=pygame.image.load("materials/canopy_night.png").convert_alpha(),can_walk_through=True)

            bg_colour = (20,30,44)
            bg = pygame.image.load('materials/background_night.png')
            bg = pygame.transform.scale(bg, ((size*100), (size*7.5)))

            food = 3000.0
            entities = [
                Enemy(x_pos=(size*2),y_pos=(size*5.5),x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*3),y_pos=(size*5.5),x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=(size*94),y_pos=(size*5.5),x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=(size*30),y_pos=(size*0.5),x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="car"),
                Enemy(x_pos=(size*50),y_pos=(size*0.5),x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*63),y_pos=(size*0.5),x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),

                    ]
            items = [
                Item(type="bucket",x_pos=(size*92), y_pos=(size*-0.5)),
                Item(type="sauce",x_pos=(size*58), y_pos=(size*2.5))
                    ]
        elif level == 3:
            #musiikki
            pygame.mixer.music.load("sound/background_music.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =polo_frames,x_pos=0,y_pos=(size*5.5),can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=(size*10),height=size,texture=pygame.image.load("materials/sand10x_snow.png").convert_alpha())
            sand = Object(width=size,height=size,texture=pygame.image.load("materials/sand_snow.png").convert_alpha())
            brick = Object(width=size,height=size,texture=pygame.image.load("materials/brick_snow.png").convert_alpha())
            brick3x = Object(width=(size*3),height=size,texture=pygame.image.load("materials/brick3x_snow.png").convert_alpha())
            lootbox_taco = Object(width=size,height=size,texture=pygame.image.load("materials/brick_snow.png").convert_alpha(),loot="taco")
            lootbox_taco1 = Object(width=size,height=size,texture=pygame.image.load("materials/brick_snow.png").convert_alpha(),loot="taco")
            well = Object(width=(size*2),height=size,texture=pygame.image.load("materials/well.png").convert_alpha())
            canopy = Object(width=(size*2),height=(size*2),texture=pygame.image.load("materials/canopy_snow.png").convert_alpha(),can_walk_through=True)

            bg_colour = (159,230,247)
            bg = pygame.image.load('materials/background_snow.png')
            bg = pygame.transform.scale(bg, ((size*100), (size*7.5)))

            food = 3000.0
            entities = [
                Enemy(x_pos=(size*7),y_pos=(size*5.5),x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*8),y_pos=(size*5.5),x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*9),y_pos=(size*5.5),x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*10),y_pos=(size*5.5),x_velocity=-2,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*25),y_pos=(size*5.5),x_velocity=2,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=(size*54),y_pos=(size*4.5),x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=(size*55),y_pos=(size*4.5),x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*56),y_pos=(size*4.5),x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*57),y_pos=(size*4.5),x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
                Enemy(x_pos=(size*80),y_pos=(size*2.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                Enemy(x_pos=(size*85),y_pos=(size*2.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                    ]
            items = [
                Item(type="bucket",x_pos=(size*95),y_pos=(size*5.5)),
                Item(type="taco",x_pos=(size*52),y_pos=(size*-2.5))
                    ]
        elif level == 4:
            #musiikki
            pygame.mixer.music.load("sound/background_music_night.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            #pelaajan alustaminen
            player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =marko_frames,x_pos=0,y_pos=(size*5.5),can_jump=False,jump_time=0,jump=-10,max_jump=30)

            sand10x = Object(width=(size*10),height=size,texture=pygame.image.load("materials/sand10x_snow_night.png").convert_alpha())
            sand = Object(width=size,height=size,texture=pygame.image.load("materials/sand_snow_night.png").convert_alpha())
            brick = Object(width=size,height=size,texture=pygame.image.load("materials/brick_snow_night.png").convert_alpha())
            brick3x = Object(width=(size*3),height=size,texture=pygame.image.load("materials/brick3x_snow_night.png").convert_alpha())
            lootbox_taco = Object(width=size,height=size,texture=pygame.image.load("materials/brick_snow_night.png").convert_alpha(),loot="taco")
            lootbox_taco1 = Object(width=size,height=size,texture=pygame.image.load("materials/brick_snow_night.png").convert_alpha(),loot="taco")
            well = Object(width=(size*2),height=size,texture=pygame.image.load("materials/well_night.png").convert_alpha())
            canopy = Object(width=(size*2),height=(size*2),texture=pygame.image.load("materials/canopy_snow_night.png").convert_alpha(),can_walk_through=True)

            bg_colour = (10,17,27)
            bg = pygame.image.load('materials/background_snow_night.png')
            bg = pygame.transform.scale(bg, ((size*100), (size*7.5)))

            food = 3000.0
            entities = [
            Enemy(x_pos=(size*5),y_pos=(size*5.5),x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
            Enemy(x_pos=(size*11),y_pos=(size*5.5),x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
            Enemy(x_pos=(size*19),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
            Enemy(x_pos=(size*58),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
            Enemy(x_pos=(size*60),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car"),
            Enemy(x_pos=(size*97),y_pos=(size*5.5),x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge"),
                ]
            items = [
                Item(type="bucket",x_pos=(size*95),y_pos=(size*-0.5))
                    ]
            
        if level >= 5:
            run = False
            prison = pygame.transform.scale(pygame.image.load('materials/background_prison.png').convert_alpha(), ((size*10), (size*7.5)))
            bliss = pygame.transform.scale(pygame.image.load('materials/background_bliss.png').convert_alpha(), ((size*10), (size*7.5)))
            policer = pygame.transform.scale(pygame.image.load('police/policer.png').convert_alpha(), (size, size))
            if marko_murderer and polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                        
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(size,(size*6.25)))
                    screen.blit(policer,((size*2.5),(size*6.25)))
                    screen.blit(policer,((size*3.75),(size*6.25)))
                    screen.blit(polo_frames[4],((size*6.25),(size*6.25)))
                    screen.blit(marko_frames[4],((size*6),(size*6)))
                    cover()
                    pygame.display.update()
                    clock.tick(60)
            elif marko_murderer and not polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(size,(size*6.25)))
                    screen.blit(policer,((size*2.5),(size*6.25)))
                    screen.blit(policer,((size*3.75),(size*6.25)))
                    screen.blit(marko_frames[4],((size*6.25),(size*6.25)))
                    cover()
                    pygame.display.update()
                    clock.tick(60)
            elif not marko_murderer and polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(size,(size*6.25)))
                    screen.blit(policer,((size*2.5),(size*6.25)))
                    screen.blit(policer,((size*3.75),(size*6.25)))
                    screen.blit(polo_frames[4],((size*6.25),(size*6.25)))
                    cover()
                    pygame.display.update()
                    clock.tick(60)
            elif not marko_murderer and not polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                    screen.blit(bliss,(0,0))
                    screen.blit(marko_frames[4],((size*1.75),(size*3)))
                    screen.blit(polo_frames[0],((size*6.25),(size*6.25)))
                    cover()
                    pygame.display.update()
                    clock.tick(60)
            is_running = False
            lives = 0
    while run:

        food -= 1
        
        screen.fill(bg_colour)
        screen.blit(bg, (global_x_offset,global_y_offset))
        if global_x_offset <= (size*-90):
            global_x_offset = (size*-90)
        #screen.blit(test_bg, (global_x_offset,global_y_offset))


        #pelaajan fysiikat ja kamera
        player.update_velocity(x_delta,gravity)

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
                fullscreen()
                    
                screen.blit(player.character[6],(player.x_pos,player.y_pos))
                cover()
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
                fullscreen()
                screen.fill(bg_colour)
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


                
                
                
                cover()
                pygame.display.update()                                       
                clock.tick(15)
            level += 1

        #ikkunan sulkeminen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        #fullscreen f11
        fullscreen()
        #pelaajan kuolema pudotukseen
        if ((player.y_pos > (size*8.75)+global_y_offset) and (player.alive) or food <= 0):
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
                player.update_velocity(x_delta,gravity)
                drawer(level,entities,items)
                screen.blit(player.character[4],(player.x_pos,player.y_pos))
                cover()
                pygame.display.update()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                fullscreen()

        #hud
        hud()
        cover()
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
    screen.blit(fontxl.render('GAME OVER',False,(255,255,255)),(size,(size*3.125)))
    pygame.display.update()
    pygame.time.delay(1000)
    score = int(score)
    ask = True
    writing = False
    yes = False
    while ask:
        fullscreen()
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
        screen.blit(font.render('press enter to save score',False,(255,255,255)),(size,(size*3.125)))
        screen.blit(font.render('press esc to continue without saving',False,(255,255,255)),(size,(size*3.5)))
        pygame.display.update()
        clock.tick(60)
    name = ""
    while writing: 
        fullscreen()
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
        screen.blit(font.render("(press esc to stop)",False,(255,255,255)),(0,(size*0.375)))
        screen.blit(fontxl.render(name,False,(255,255,255)),(size,(size*3.125)))
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
        score_board()
        pygame.display.update()
        clock.tick(60)
        fullscreen()
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
