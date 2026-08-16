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
# i am not a lie

import pygame, json, csv
screensize = (800, 600)

SIZE = 80
print(SIZE)
print(screensize)
#pygamen initialisaatio
pygame.init()
pygame.mixer.init()

jsonFile = json.loads(open("sos.json").read())
is_running = True
lives = 3
level = 1
try:
    final_level = jsonFile["misc"]["levels"]
except:
    final_level = 1
score = 0
polo_murderer = False
marko_murderer = False
f11_timeout = True
t_velocity = 9

#näytön asetuksia

SCREEN_WIDTH = SIZE*10
SCREEN_HEIGHT = SIZE*7.5
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SCALED)

windowsize = pygame.display.get_window_size()
print(windowsize)
#ikkunan nimi
pygame.display.set_caption("Super Marko Brothers")
#ikkunan kuvake
pygame.display.set_icon(pygame.image.load('./resources/textures/Smb_ico.png'))
#fontti
font =pygame.font.Font('freesansbold.ttf', int((SIZE*0.4)))
fontxl =pygame.font.Font('freesansbold.ttf', int((SIZE*1.25)))

jump_sound = pygame.mixer.Sound("./resources/sound/jump.wav")
jump_sound.set_volume(0.01)
taco_sound = pygame.mixer.Sound("./resources/sound/taco_sound.wav")
taco_sound.set_volume(0.01)


#pelin elollisten olijoiden attributejen tallennukseen käytettävä classi
class Attribute:
    def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float,character, x_pos:float, y_pos:float, can_jump:bool, jump_time:int, jump:int, max_jump:int):
        self.y_velocity = y_velocity #tämän hetkinen nopeus
        self.x_velocity = x_velocity #tämän hetkinen nopeus
        self.on_ground = bool(on_ground) #onko pelaaja maassa
        self.speed = speed *(SIZE/80)# mikä on pelaajan kiihtyvyys
        self.character = characters[character] #onko pelaaja polo vai marko
        self.x_pos = x_pos #pelaajan lokaatio
        self.y_pos = y_pos #pelaajan lokaatio
        self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,SIZE,SIZE) #pelaajan hitbox
        self.can_jump = bool(can_jump) #voiko pelaaja hyppiä
        self.jump_time = jump_time #kuinks pitkään pelaaja on hypännyt
        self.jump = jump * (SIZE/80) #pelaajan hyppy voima
        self.max_jump = max_jump #aika hz
        self.alive = True #onko pelaaja hengissä
        self.frameid = 0 #pelaajan tämän hetkinen animaatio kehys
        self.delay = 0 #animaation kehysten välinen viive tällä hetkellä
        self.frame_count = 4 #kuinka monta kehystä animaatiossa on (kävely ei muut)
        self.flip = False
    def __str__(self):
        return f" x_velocity={self.x_velocity}, y_velocity={self.y_velocity}"
    def update_velocity(self, x_delta, gravity):
        if self.y_velocity > t_velocity*(SIZE/80):
            self.y_velocity = t_velocity*(SIZE/80)
        else:
            self.y_velocity += gravity
        self.x_velocity = self.x_velocity * x_delta 
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        
        self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,SIZE,SIZE)

        


    def camera(self):
        global global_x_offset
        global global_y_offset
        
        if self.x_pos >= 400*(SIZE/80):
            self.x_pos = (400*(SIZE/80))-1
            if self.x_velocity > 0:
                global_x_offset -= self.x_velocity
            else:
                global_x_offset += self.x_velocity
        if self.y_pos <= 50*(SIZE/80):
            self.y_pos = (50*(SIZE/80))-1
            global_y_offset -= self.y_velocity
        if (self.y_pos >= 50*(SIZE/80)) and (not global_y_offset < 1*(SIZE/80)):
            self.y_pos = 50*(SIZE/80)
            global_y_offset -= self.y_velocity
        if global_y_offset <= 0:
            global_y_offset = 0
        if self.x_pos <= 0:
            self.x_pos = 0
            self.x_velocity = 0                                   
        if self.x_pos >= SIZE*10:
            self.x_pos = (SIZE*10)-1
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
            print((self.x_pos-global_x_offset),(self.y_pos-global_y_offset))
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
                if self.flip:
                    screen.blit(pygame.transform.flip(self.character[5],True,False),(self.x_pos,self.y_pos))
                else:
                    screen.blit(self.character[5],(self.x_pos,self.y_pos))
            elif key[pygame.K_a] == True:
                self.flip = True
                self.x_velocity += -self.speed
                screen.blit(pygame.transform.flip(self.character[5],True,False),(self.x_pos,self.y_pos))
            elif key[pygame.K_d] == True:
                self.flip = False
                self.x_velocity += self.speed
                screen.blit(self.character[5],(self.x_pos,self.y_pos))
            else:
                if self.flip:
                    screen.blit(pygame.transform.flip(self.character[5],True,False),(self.x_pos,self.y_pos))
                else:
                    screen.blit(self.character[5],(self.x_pos,self.y_pos))
        elif (self.jump_time > 0) and (self.can_jump):
            self.jump_time += self.max_jump + 100
            screen.blit(self.character[5],(self.x_pos,self.y_pos))   
        #kävely
        elif (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
            if self.flip:
                screen.blit(pygame.transform.flip(self.character[0],True,False),(self.x_pos,self.y_pos))
            else:
                screen.blit(self.character[0],(self.x_pos,self.y_pos))
        elif key[pygame.K_a] == True:
            self.flip = True
            self.x_velocity += -self.speed
            screen.blit(pygame.transform.flip(self.character[self.frameid],True,False),(self.x_pos,self.y_pos))
        elif key[pygame.K_d] == True:
            self.flip = False
            self.x_velocity += self.speed
            screen.blit(self.character[self.frameid],(self.x_pos,self.y_pos))
        else:
            if self.flip:
                screen.blit(pygame.transform.flip(self.character[0],True,False),(self.x_pos,self.y_pos))
            else:
                screen.blit(self.character[0],(self.x_pos,self.y_pos))


class Object:
    def __init__(self,width:int,height:int,texture,loot:str=None,collision:bool=True):
        self.width = width
        self.height = height
        self.loot = loot
        self.texture = pygame.transform.scale(texture,(self.width,self.height))
        self.collision = collision
    def draw(self,lista:list,entities:list=None):
        global global_x_offset
        global touch
        
        for location in lista:
            screen.blit(self.texture,(global_x_offset + location[0],global_y_offset + location[1]))
            if player.alive:
                if self.collision == True:
                    #osumat palikan päällä
                    if (location[1] < player.y_pos-global_y_offset + SIZE < location[1] +(SIZE/4)) and ( location[0]-SIZE+(SIZE/8) < player.x_pos-global_x_offset <location[0]+self.width-(SIZE/8)):
                        player.y_pos = global_y_offset + location[1] - self.height
                        player.y_velocity = 0
                        player.on_ground = True
                        touch = True

                    #osumat palikan alla
                    if (location[1] +self.height >= player.y_pos-global_y_offset >= location[1] +self.height -(SIZE/4)) and (location[0]-SIZE+(SIZE/8) <= player.x_pos-global_x_offset <= location[0]+self.width-(SIZE/8)):
                        player.y_pos = global_y_offset + location[1] +self.height
                        player.y_velocity = 0
                        if not self.loot == 0:
                            items.append(Item(type=self.loot,x_pos=global_x_offset + location[0],y_pos=global_y_offset + location[1]-SIZE))
                            self.loot = 0

                    #osumat palikan oikea laita
                    if (location[0] <= player.x_pos+SIZE -global_x_offset <= location[0] +(SIZE/4)) and (location[1]+(SIZE/8) <= player.y_pos +SIZE -global_y_offset <= location[1]+self.height+SIZE-(SIZE/8)):
                        player.x_pos = global_x_offset + location[0] -SIZE

                    #osumat palikan vasen laita
                    if (location[0] + self.width >= player.x_pos-global_x_offset >= location[0]-(SIZE/4)) and (location[1]+(SIZE/8) <= player.y_pos +SIZE -global_y_offset <= location[1]+self.height+SIZE-(SIZE/8)):
                        player.x_pos = global_x_offset + location[0] +self.width
                       

            if not entities == None:
            #npc osumat        
                for entity in entities:
                    for location in lista:
                        #osumat palikan päällä
                        if (location[1] < entity.y_pos + SIZE < location[1] +(SIZE/4)) and (location[0]-SIZE < entity.x_pos < location[0]+self.width):
                            entity.y_pos = location[1] - self.height 
                            entity.y_velocity = 0


                        #osumat palikan alla
                        if (location[1] +self.height >= entity.y_pos >= location[1] +self.height -(SIZE/4)) and (location[0]-SIZE <= entity.x_pos <= location[0]+self.width):
                            entity.y_pos = location[1] +self.height 

                        #osumat palikan vasen laita
                        if (location[0] <= entity.x_pos +SIZE <= location[0] +(SIZE/4)) and (location[1]+(SIZE/8) <= entity.y_pos +SIZE <= location[1]+self.height+SIZE-(SIZE/8)):
                            entity.x_pos = location[0] -SIZE
                            if entity.x_velocity > 0:
                                entity.x_velocity = -entity.x_velocity
                            
                        #osumat palikan oikea laita
                        if (location[0] + self.width >= entity.x_pos >= location[0]-(SIZE/4)) and (location[1]+(SIZE/8) <= entity.y_pos +SIZE <= location[1]+self.height+SIZE-(SIZE/8)):
                            entity.x_pos = location[0] +self.width 
                            if entity.x_velocity < 0:
                                entity.x_velocity = -entity.x_velocity
                            
class Enemy:        
    def __init__(self, y_velocity:float, x_velocity:float,x_pos:int,y_pos:int, frame_count:int, anim_speed:int, type:int, character:int):
        self.y_velocity = y_velocity
        self.x_velocity = x_velocity * (SIZE/80)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.frameid = 0
        self.delay = 0
        self.anim_speed = anim_speed
        self.frame_count = frame_count
        if character == 0:
            self.character = characters[3]
        elif character == 1:
            self.character = characters[2]
        self.rect = pygame.rect.Rect(self.x_pos+(SIZE/8)+global_x_offset,self.y_pos+global_y_offset+(SIZE/8),(SIZE*0.75),(SIZE*0.75))
        self.type = type
        self.flip = False
    def update(self,gravity:float):
        if self.y_velocity > t_velocity*(SIZE/80):
            self.y_velocity = t_velocity*(SIZE/80)
        else:
            self.y_velocity += gravity*(SIZE/80)
        
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        
        self.rect = pygame.rect.Rect(self.x_pos+(SIZE/8)+global_x_offset,self.y_pos+global_y_offset+(SIZE/8),(SIZE*0.75),(SIZE*0.75))
        
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
    def __init__(self,type:int,x_pos:int,y_pos:int):
        self.type = type
        self.x_pos = x_pos
        self.y_pos = y_pos
        if type == 1:
            self.texture = pygame.transform.scale(pygame.image.load('./resources/textures/items/taco.png').convert_alpha(),(SIZE,SIZE))
        elif type == 2:
            self.texture = pygame.transform.scale(pygame.image.load('./resources/textures/items/sauce.png').convert_alpha(),(SIZE,SIZE))
        elif type == 3:
            self.texture = pygame.transform.scale(pygame.image.load('./resources/textures/items/bucket.png').convert_alpha(),(SIZE,SIZE))
        else:
            self.texture = pygame.transform.scale(pygame.image.load('./resources/textures/items/taco.png').convert_alpha(),(SIZE,SIZE))
        self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,SIZE,SIZE)
    
    def draw(self):
        screen.blit(self.texture,(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
        self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,SIZE,SIZE)


def loader(level:int):
    global sand10x_list
    global sand_list
    global brick3x_list
    global brick_list
    global lootbox_taco_list
    global well_list
    global canopy_list
    global sand10x
    global sand
    global brick3x
    global brick
    global lootbox_taco
    global well
    global canopy
    global entities
    global items
    global food
    global player
    global is_running
    global bg_colour
    global bg
    sand10x_list = []
    sand_list = []
    brick3x_list = []
    brick_list = []
    lootbox_taco_list = []
    well_list = []
    canopy_list = []
    try:
        for i in jsonFile["levels"][level-1]["platforms"]:
            for location in jsonFile["levels"][level-1]["platforms"][i]:
                if (type(location["y"]) is float or type(location["y"]) is int) and (type(location["x"]) is float or type(location["x"]) is int):
                    if i == "sand10x":
                        sand10x_list.append(((location["x"]*SIZE),location["y"]*SIZE))
                    elif i == "sand":
                        sand_list.append(((location["x"]*SIZE),location["y"]*SIZE))
                    elif i == "brick3x":
                        brick3x_list.append(((location["x"]*SIZE),location["y"]*SIZE))
                    elif i == "brick":
                        brick_list.append(((location["x"]*SIZE),location["y"]*SIZE))
                    elif i == "lootbox_taco":
                        lootbox_taco_list.append(((location["x"]*SIZE),location["y"]*SIZE))
                    elif i == "well":
                        well_list.append(((location["x"]*SIZE),location["y"]*SIZE))
                    elif i == "canopy":
                        canopy_list.append(((location["x"]*SIZE),location["y"]*SIZE))
                else:
                    print("type error while loading platform fix or else")
    except:
        raise SystemError("json")
    try:
        entities = []
        for i in jsonFile["levels"][level-1]["entities"]:
            if ((type(i["x"]) is int or type(i["x"] is float)) and 
                (type(i["y"]) is int or type(i["y"] is float)) and 
                (type(i["x_velocity"]) is int or type(i["x_velocity"] is float)) and 
                (type(i["y_velocity"]) is int or type(i["y_velocity"] is float)) and 
                (type(i["frame_count"]) is int) and 
                (type(i["anim_speed"]) is int or type(i["anim_speed"] is float)) and 
                (type(i["type"]) is int) and 
                (type(i["character"]) is int)):
                entities.append(Enemy(x_pos=(SIZE*i["x"]),y_pos=(SIZE*i["y"]),x_velocity=i["x_velocity"],y_velocity=i["y_velocity"],frame_count=i["frame_count"],anim_speed=i["anim_speed"],type=i["type"],character=i["character"]))
            else:
                print("type error while loading entity fix or else")
    except:
        raise SystemError("json")
    try:
        items = []
        for i in jsonFile["levels"][level-1]["items"]:

            if (type(i["type"]) is int) and (type(i["x"]) is int or type(i["x"]) is float) and (type(i["y"]) is int or type(i["y"]) is float):
                items.append(Item(type=i["type"],x_pos=(i["x"]*SIZE),y_pos=(i["y"]*SIZE)))
                
            else:
                print("type error while loading items fix or else")
    except:
        raise SystemError("json")
    try:
        for i in jsonFile["levels"][level-1]["misc"]:
            temp_dict = {}
            if i == "food":
                if type(jsonFile["levels"][level-1]["misc"][i]) is int or type(jsonFile["levels"][level-1]["misc"][i]) is float:
                    food = jsonFile["levels"][level-1]["misc"][i]
            elif i == "music":
                if type(jsonFile["levels"][level-1]["misc"][i]) is str:
                    pygame.mixer.music.load(f'./resources/{jsonFile["levels"][level-1]["misc"][i]}')
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
            elif i == "playerAttribute":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["y_velocity"]) is int or type(temp_dict["y_velocity"] is float)) and 
                    (type(temp_dict["x_velocity"]) is int or type(temp_dict["x_velocity"] is float)) and
                    (type(temp_dict["on_ground"]) is int) and
                    (type(temp_dict["speed"]) is int or type(temp_dict["speed"] is float)) and
                    (type(temp_dict["character"]) is int) and
                    (type(temp_dict["x_pos"]) is int or type(temp_dict["x_pos"] is float)) and
                    (type(temp_dict["y_pos"]) is int or type(temp_dict["y_pos"] is float)) and
                    (type(temp_dict["can_jump"]) is int) and
                    (type(temp_dict["jump_time"]) is int or type(temp_dict["jump_time"] is float)) and
                    (type(temp_dict["jump"]) is int or type(temp_dict["jump"] is float)) and
                    (type(temp_dict["max_jump"]) is int or type(temp_dict["max_jump"] is float))
                    ):
                    player = Attribute(y_velocity=temp_dict["y_velocity"], x_velocity=temp_dict["x_velocity"], on_ground=temp_dict["on_ground"], speed=temp_dict["speed"],character=temp_dict["character"],x_pos=temp_dict["x_pos"]*SIZE,y_pos=temp_dict["y_pos"]*SIZE,can_jump=temp_dict["can_jump"],jump_time=temp_dict["jump_time"],jump=temp_dict["jump"],max_jump=temp_dict["max_jump"])

            elif i == "sand10x":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and
                    (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and
                    (type(temp_dict["texture"]) is str) and
                    (type(temp_dict["loot"]) is int) and
                    (type(temp_dict["collision"]) is int)
                    ):
                    sand10x = Object(width=temp_dict["width"]*SIZE,height=temp_dict["height"]*SIZE,texture=pygame.image.load(f'./resources/{temp_dict["texture"]}').convert_alpha(),loot=temp_dict["loot"],collision=temp_dict["collision"])
            elif i == "sand":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and
                    (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and
                    (type(temp_dict["texture"]) is str) and
                    (type(temp_dict["loot"]) is int) and
                    (type(temp_dict["collision"]) is int)
                    ):
                    sand = Object(width=temp_dict["width"]*SIZE,height=temp_dict["height"]*SIZE,texture=pygame.image.load(f'./resources/{temp_dict["texture"]}').convert_alpha(),loot=temp_dict["loot"],collision=temp_dict["collision"])
            elif i == "brick":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and
                    (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and
                    (type(temp_dict["texture"]) is str) and
                    (type(temp_dict["loot"]) is int) and
                    (type(temp_dict["collision"]) is int)
                    ):
                    brick = Object(width=temp_dict["width"]*SIZE,height=temp_dict["height"]*SIZE,texture=pygame.image.load(f'./resources/{temp_dict["texture"]}').convert_alpha(),loot=temp_dict["loot"],collision=temp_dict["collision"])
            elif i == "brick3x":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and
                    (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and
                    (type(temp_dict["texture"]) is str) and
                    (type(temp_dict["loot"]) is int) and
                    (type(temp_dict["collision"]) is int)
                    ):
                    brick3x = Object(width=temp_dict["width"]*SIZE,height=temp_dict["height"]*SIZE,texture=pygame.image.load(f'./resources/{temp_dict["texture"]}').convert_alpha(),loot=temp_dict["loot"],collision=temp_dict["collision"])
            elif i == "lootbox_taco":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and
                    (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and
                    (type(temp_dict["texture"]) is str) and
                    (type(temp_dict["loot"]) is int) and
                    (type(temp_dict["collision"]) is int)
                    ):
                    lootbox_taco = Object(width=temp_dict["width"]*SIZE,height=temp_dict["height"]*SIZE,texture=pygame.image.load(f'./resources/{temp_dict["texture"]}').convert_alpha(),loot=temp_dict["loot"],collision=temp_dict["collision"])
            elif i == "well":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and
                    (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and
                    (type(temp_dict["texture"]) is str) and
                    (type(temp_dict["loot"]) is int) and
                    (type(temp_dict["collision"]) is int)
                    ):
                    well = Object(width=temp_dict["width"]*SIZE,height=temp_dict["height"]*SIZE,texture=pygame.image.load(f'./resources/{temp_dict["texture"]}').convert_alpha(),loot=temp_dict["loot"],collision=temp_dict["collision"])
            elif i == "canopy":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if ((type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and
                    (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and
                    (type(temp_dict["texture"]) is str) and
                    (type(temp_dict["loot"]) is int) and
                    (type(temp_dict["collision"]) is int)
                    ):
                    canopy = Object(width=temp_dict["width"]*SIZE,height=temp_dict["height"]*SIZE,texture=pygame.image.load(f'./resources/{temp_dict["texture"]}').convert_alpha(),loot=temp_dict["loot"],collision=temp_dict["collision"])
            elif i == "bg_colour":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if (type(temp_dict["r"]) is int) and (type(temp_dict["g"]) is int) and (type(temp_dict["b"]) is int):
                    bg_colour = (temp_dict["r"],temp_dict["g"],temp_dict["b"])
            elif i == "bg":
                temp_dict = jsonFile["levels"][level-1]["misc"][i]
                if (type(temp_dict["width"]) is int or type(temp_dict["width"]) is float) and (type(temp_dict["height"]) is int or type(temp_dict["height"]) is float) and (type(temp_dict["texture"]) is str):
                    bg = pygame.transform.scale(pygame.image.load(f'./resources/{temp_dict["texture"]}'), ((SIZE*100), (SIZE*7.5)))
    except:
        raise SystemError("json")
                
    return
    
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
            if item.type == 3:
                win = True
            elif item.type == 1:
                taco_sound.play()
                food += 1000
                lives += 1
            elif item.type == 2:
                lives += 1
    for take in collect:
        items.remove(take)
    for item in items:
        if (item.x_pos <= -global_x_offset + (SIZE*10)):
            item.draw()
            




    ded = []
    # npc kuolemat ja tapot
    for entity in entities:
        if entity.y_pos >= (SIZE*8.75):
            ded.append(entity)


        if entity.type == 1:
            if (entity.x_pos + global_x_offset+(SIZE/16) <= player.x_pos+SIZE <= entity.x_pos +(SIZE*2)+ global_x_offset-(SIZE/16)) and (entity.y_pos+global_y_offset-SIZE-(SIZE/4) <= player.y_pos <= entity.y_pos+global_y_offset-SIZE) and (player.y_velocity > 0): 
                
                ded.append(entity)
                player.y_velocity = player.jump
                current_level_score += 100
                has_killed = True
            elif pygame.Rect.colliderect(entity.rect,player.rect):
                
                player.alive = False 


        elif entity.type == 0:
            if (entity.x_pos + global_x_offset+(SIZE/8) <= player.x_pos+SIZE <= entity.x_pos +(SIZE*2)+ global_x_offset-(SIZE/8)) and (entity.y_pos+global_y_offset-SIZE-(SIZE/4) <= player.y_pos <= entity.y_pos+global_y_offset-SIZE) and (player.y_velocity > 0): 
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
                if (i.y_pos + global_y_offset < entity.y_pos + SIZE < i.y_pos + global_y_offset +(SIZE/4)) and (i.x_pos + global_x_offset-SIZE < entity.x_pos + global_x_offset < i.x_pos + global_x_offset+SIZE):
                    entity.y_pos = i.y_pos -SIZE
                    entity.y_velocity = 0
                #osumat olion alla
                if (i.y_pos+ global_y_offset +SIZE >= entity.y_pos >= i.y_pos+ global_y_offset +SIZE -(SIZE/4)) and (i.x_pos + global_x_offset-SIZE <= entity.x_pos + global_x_offset <= i.x_pos + global_x_offset+SIZE):
                    entity.y_pos = i.y_pos +SIZE

                #osumat olion vasen laita
                if (i.x_pos+ + global_x_offset <= entity.x_pos + global_x_offset+SIZE <= i.x_pos + global_x_offset +(SIZE/4)) and (i.y_pos+(SIZE/8)+global_y_offset <= entity.y_pos +SIZE <= i.y_pos+SIZE+SIZE-(SIZE/8)+global_y_offset):
                    entity.x_pos = i.x_pos -SIZE 
                    if entity.x_velocity > 0:
                        entity.x_velocity = -entity.x_velocity

                #osumat polion oikea laita
                if (i.x_pos + global_x_offset + SIZE >= entity.x_pos + global_x_offset >= i.x_pos + global_x_offset-(SIZE/4)) and (i.y_pos+(SIZE/8)+global_y_offset <= entity.y_pos +SIZE <= i.y_pos+SIZE+SIZE-(SIZE/8)+global_y_offset):
                    entity.x_pos = i.x_pos +SIZE
                    if entity.x_velocity < 0:
                        entity.x_velocity = -entity.x_velocity
    for bury in ded:
        entities.remove(bury)
    for entity in entities:
        if not entity.x_pos >= -global_x_offset + (SIZE*12.5):
            entity.update(gravity)

    if 1 <= level <= final_level:
        
        touch = False
        sand10x.draw(sand10x_list,entities)
        sand.draw(sand_list,entities)
        brick3x.draw(brick3x_list,entities)
        brick.draw(brick_list,entities)
        lootbox_taco.draw(lootbox_taco_list,entities)
        well.draw(well_list,entities)
        canopy.draw(canopy_list,entities)

        if touch == False:
            player.on_ground = False

def hud():
    #hud
    screen.blit(font.render("lives",False,(0,0,0)),(SIZE*8.125,0))
    screen.blit(font.render(f"{lives}",False,(0,0,0)),(SIZE*8.75,SIZE*0.625))
    screen.blit(font.render("food",False,(0,0,0)),(SIZE*3.125,0))
    if food//10 >= 100:
        screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(SIZE*3.25,SIZE*0.625))
    elif food//10 >= 10:
        screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(SIZE*3.5,SIZE*0.625))
    else:
        screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(SIZE*3.75,SIZE*0.625))

    screen.blit(font.render("level",False,(0,0,0)),(SIZE*5.625,0))
    screen.blit(font.render(f"{level}",False,(0,0,0)),(SIZE*6.25,SIZE*0.625))
    screen.blit(font.render("score",False,(0,0,0)),(SIZE*0.625,0))
    screen.blit(font.render(f"{int(score+current_level_score)}",False,(0,0,0)),(SIZE*1.25,SIZE*0.625))

def score_board():
    screen.fill((0,0,0))
    for i in range(0,12):
        screen.blit(font.render(f"{i+1+scroll}",False,(255,255,255)),(0,i*50))
        screen.blit(font.render(high_scores[scroll+i][0],False,(255,255,255)),(100,i*50))
        screen.blit(font.render(high_scores[scroll+i][1],False,(255,255,255)),(400,i*50))

def fullscreen():
    global f11_timeout
    key = pygame.key.get_pressed()
    if key[pygame.K_F11] and f11_timeout:
        pygame.display.toggle_fullscreen()
        f11_timeout = False
    elif not key[pygame.K_F11] and not f11_timeout:
        f11_timeout = True
def player_death():
    global run
    global lives
    lives -= 1
    run = False
    player.x_velocity = 0
    player.y_velocity = 0
    if level == 1 or level == 3:
        pygame.mixer.music.load("./resources/sound/deadin1.wav")
    elif level == 2 or level == 4:
        pygame.mixer.music.load("./resources/sound/deadin2.wav")
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

        pygame.display.update()
        clock.tick(60)

def level_win():
    global polo_murderer
    global marko_murderer
    global run
    global current_level_score
    global score
    global level
    if player.character == characters[0] and has_killed:
        polo_murderer = True
    elif player.character == characters[1] and has_killed:
        marko_murderer = True

    current_level_score += food//10*10
    score += current_level_score
    pygame.mixer.music.load("./resources/sound/winnin.wav")
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


        
        
        

        pygame.display.update()                                       
        clock.tick(15)
    level += 1

characters = []
polo_frames = []
for i in range(1, 8):
    frame = pygame.image.load(f'./resources/textures/Polo/Polo{i}.png').convert_alpha()  
    frame = pygame.transform.scale(frame,(SIZE,SIZE))
    polo_frames.append(frame)
characters.append(polo_frames)
#pelaajan polo animaatio framejen tuonti
marko_frames = []
for i in range(1, 8):
    frame = pygame.image.load(f'./resources/textures/marko/marko{i}.png').convert_alpha()  
    frame = pygame.transform.scale(frame,(SIZE,SIZE))
    marko_frames.append(frame)
characters.append(marko_frames)
#koiruli framet
doge_frames = []
for i in range(1, 3):
    frame = pygame.image.load(f'./resources/textures/doge/doge{i}.png').convert_alpha()  
    frame = pygame.transform.scale(frame,(SIZE,SIZE))
    doge_frames.append(frame)
characters.append(doge_frames)
#auton framet
car_frames = []
for i in range(1, 7):
    frame = pygame.image.load(f'./resources/textures/car/car{i}.png').convert_alpha()  
    frame = pygame.transform.scale(frame,(SIZE,SIZE))
    car_frames.append(frame)
characters.append(car_frames)

while is_running:
    has_killed = False
    #pelaajan polo animaatio framejen tuonti

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
        #putoamis nopeus pixeliä framessa
        gravity = 1.1*(SIZE/80)

        #testbg
        test_bg = pygame.transform.scale(pygame.image.load('./resources/textures/materials/background_test.png'), ((SIZE*100), (SIZE*7.5)))
        #level 1
        bg_colour = (0,0,0)
        if level <= final_level:
            
            loader(level)
            
        else:
            run = False
            prison = pygame.transform.scale(pygame.image.load('./resources/textures/materials/background_prison.png').convert_alpha(), ((SIZE*10), (SIZE*7.5)))
            bliss = pygame.transform.scale(pygame.image.load('./resources/textures/materials/background_bliss.png').convert_alpha(), ((SIZE*10), (SIZE*7.5)))
            policer = pygame.transform.scale(pygame.image.load('./resources/textures/police/policer.png').convert_alpha(), (SIZE, SIZE))
            if marko_murderer and polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                        
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(SIZE,(SIZE*6.25)))
                    screen.blit(policer,((SIZE*2.5),(SIZE*6.25)))
                    screen.blit(policer,((SIZE*3.75),(SIZE*6.25)))
                    screen.blit(characters[0][4],((SIZE*6.25),(SIZE*6.25)))
                    screen.blit(characters[1][4],((SIZE*6),(SIZE*6)))

                    pygame.display.update()
                    clock.tick(60)
            elif marko_murderer and not polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(SIZE,(SIZE*6.25)))
                    screen.blit(policer,((SIZE*2.5),(SIZE*6.25)))
                    screen.blit(policer,((SIZE*3.75),(SIZE*6.25)))
                    screen.blit(characters[1][4],((SIZE*6.25),(SIZE*6.25)))

                    pygame.display.update()
                    clock.tick(60)
            elif not marko_murderer and polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                    screen.blit(prison,(0,0))
                    screen.blit(policer,(SIZE,(SIZE*6.25)))
                    screen.blit(policer,((SIZE*2.5),(SIZE*6.25)))
                    screen.blit(policer,((SIZE*3.75),(SIZE*6.25)))
                    screen.blit(characters[0][4],((SIZE*6.25),(SIZE*6.25)))

                    pygame.display.update()
                    clock.tick(60)
            elif not marko_murderer and not polo_murderer:
                for t in range(120):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    fullscreen()
                    screen.blit(bliss,(0,0))
                    screen.blit(characters[1][4],((SIZE*1.75),(SIZE*3)))
                    screen.blit(characters[0][0],((SIZE*6.25),(SIZE*6.25)))

                    pygame.display.update()
                    clock.tick(60)
            is_running = False
            lives = 0
    while run:

        food -= 1
        
        screen.fill(bg_colour)
        screen.blit(bg, (global_x_offset,global_y_offset))
        if global_x_offset <= (SIZE*-90):
            global_x_offset = (SIZE*-90)
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
            player_death()
            
        if win:  
            level_win()
        #ikkunan sulkeminen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        #fullscreen f11
        fullscreen()
        #pelaajan kuolema pudotukseen
        if (((player.y_pos > (SIZE*8.75)+global_y_offset) and (player.alive)) or food <= 0):
            
            lives -= 1
            run = False
            if level == 1 or level == 3:
                pygame.mixer.music.load("./resources/sound/deadin1.wav")
            elif level == 2 or level == 4:
                pygame.mixer.music.load("./resources/sound/deadin2.wav")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(1)
            for i in range(120):
                screen.fill(bg_colour)
                screen.blit(bg, (global_x_offset,global_y_offset))
                player.update_velocity(x_delta,gravity)
                drawer(level,entities,items)
                screen.blit(player.character[4],(player.x_pos,player.y_pos))

                pygame.display.update()
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                fullscreen()

        #hud
        hud()
        #näytön päyivitys
        pygame.display.update()

        #suorituksen nopeus
        clock.tick(60)
if lives <= 0:
    #musiikki
    pygame.mixer.music.load("./resources/sound/background_music_best.wav")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    screen.fill((0,0,0))
    screen.blit(fontxl.render('GAME OVER',False,(255,255,255)),(SIZE,(SIZE*3.125)))
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
        screen.blit(font.render('press enter to save score',False,(255,255,255)),(SIZE,(SIZE*3.125)))
        screen.blit(font.render('press esc to continue without saving',False,(255,255,255)),(SIZE,(SIZE*3.5)))
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
        screen.blit(font.render("(press esc to stop)",False,(255,255,255)),(0,(SIZE*0.375)))
        screen.blit(fontxl.render(name,False,(255,255,255)),(SIZE,(SIZE*3.125)))
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
