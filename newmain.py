import pygame
from pygame.locals import *
from pygame import mixer
import random
import os
import sys
import math

# pylint : disable=no-member

STROKE_SIZE = 1

pygame.init()

W,H = 800,600
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Day&Night')
icon = pygame.image.load('dragon.png')
pygame.display.set_icon(icon)
mixer.music.load('bgm.wav')
mixer.music.play(-1)
global move_sound
global poo_collision_sound
global clover_collision_sound
global score
move_sound = pygame.mixer.Sound('playerupdown.wav')
poo_collision_sound=pygame.mixer.Sound('poo.wav')
clover_collision_sound=pygame.mixer.Sound('clover.wav')

bg=pygame.image.load('d_n.jpg')
# global bgX
bgX=0
# global bgX2
bgX2= bg.get_width() #800

clock=pygame.time.Clock()

def RectMakeCenter(cx, cy, width, height):
    return (cx - width // 2, cy - height // 2, width, height)

class player(object):
    player = pygame.image.load('dragon.png')
    fall= pygame.image.load('dragon_collision.png')
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.up = False
        self.down = False
        self.falling=False
        self.hitbox = RectMakeCenter(self.x+self.width//2,self.y+self.height//2,self.width//2,self.height//2)
    def draw(self,win):
        if self.falling:
            win.blit(self.fall,(self.x,self.y))
            self.hitbox = RectMakeCenter(self.x+self.width//2,self.y+self.height//2,self.width//2,self.height//2)
            
            if self.up:
                self.y -= 5
                win.blit(self.fall,(self.x,self.y))
                self.falling=False
                self.up=False

            if self.down:
                self.y += 5
                win.blit(self.fall,(self.x,self.y))
                self.falling=False
                self.down=False
        else:
            win.blit(self.player,(self.x,self.y))
            self.hitbox = RectMakeCenter(self.x+self.width//2,self.y+self.height//2,self.width//2,self.height//2)
            if self.up:
                self.y -= 5
                win.blit(self.player,(self.x,self.y))
                self.up=False
            if self.down:
                self.y += 5
                win.blit(self.player,(self.x,self.y))
                self.down=False

        
        #pygame.draw.rect(win,(255,0,0),self.hitbox,STROKE_SIZE)
        
class poo(object):
    poo = pygame.image.load("poo.png")
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hitbox = (self.x,self.y,self.width,self.height)
    def draw(self,win):
        self.hitbox = (self.x,self.y,self.width,self.height)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,STROKE_SIZE)

        win.blit(self.poo,(self.x,self.y))
        if random.randint(0,2)==0:
            self.x=self.x-15
            self.y=self.y+3
        if random.randint(0,2)==1:
            self.x=self.x-15
            self.y=self.y-3

    def collide(self,rect):
        if rect[0] <= self.hitbox[0]+self.hitbox[2] and self.hitbox[0] <= rect[0]+rect[2]:
            if rect[1] <=self.hitbox[1]+self.hitbox[3] and self.hitbox[1] <=rect[1]+rect[3]:
                return True
        return False

class clover(object):
    clover=pygame.image.load("clover.png")
    clover1=pygame.image.load("clover1.png")
    clover2=pygame.image.load("clover2.png")
    def __init__(self, x,y, width,height):
        self.x =x
        self.y =y
        self.width =width
        self.height=height
        self.hitbox = (self.x,self.y,self.width,self.height)
    def draw(self,win):
        self.hitbox = (self.x,self.y,self.width,self.height)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,STROKE_SIZE)
        chance = random.randint(0,3)
        if chance==0: 
            win.blit(self.clover,(self.x,self.y))
            self.x=self.x-15
            self.y=self.y+3
        elif chance==1:
            win.blit(self.clover1,(self.x,self.y))
            self.x=self.x-10
            self.y=self.y+3
        else:
            win.blit(self.clover2,(self.x,self.y))
            self.x=self.x-15
            self.y=self.y-3
    def collide(self,rect):
        if rect[0] <= self.hitbox[0]+self.hitbox[2] and self.hitbox[0] <= rect[0]+rect[2]:
            if rect[1] <=self.hitbox[1]+self.hitbox[3] and self.hitbox[1] <=rect[1]+rect[3]:
                return True
        return False

class heart(object):
    heart=pygame.image.load("whiteheart.png")
    def __init__(self, x,y, width,height):
        self.x =x
        self.y =y
        self.width =width
        self.height=height
    def draw(self,win):
        win.blit(self.heart,(self.x,self.y))
          
#시간흐름에따라 백그라운드 움직이는 속도 증가시키고 싶으면
#타이머이벤트를 써야한다.
#everytime the timer goes off we will increase the speed and reset the timer

def updateFile():
    f=open('scores.txt','r')
    file=f.readlines()
    last=int(file[0])

    if last <int(score):
        f.close()
        file = open('scores.txt','w')
        file.write(str(score))
        file.close()

        return score
    return last

def endScreen():
   dragon = pygame.image.load('Bigdragon.png')
   ending =True

   while ending:
       
        for event in pygame.event. get():
            win.fill((255,216,209))
            win.blit(dragon,(200,150))
            largeFont = pygame.font.SysFont('C:\Windows\Fonts\Bahnschrift.ttf',120)
            largeFont2 = pygame.font.SysFont('C:\Windows\Fonts\Bahnschrift.ttf',50)
            lastScore=largeFont2.render('Best Score : '+str(updateFile()),1,(0,0,0))
            currentScore=largeFont2.render('Score: '+str(score),1,(0,0,0))
            win.blit(lastScore, (430, 220))
            win.blit(currentScore, (430, 260))

            text = largeFont.render('Game Over',True,(0,0,0))
            again_text=largeFont2.render('Again',True,(255,255,255))
            quit_text=largeFont2.render('Quit',True,(255,255,255))
            win.blit(text,(170,400))

            mouse=pygame.mouse.get_pos()
            click=pygame.mouse.get_pressed()

            #(200,500,150,50) (400,500,150,50)
            if(200+150>mouse[0]>200 and 500+50>mouse[1]>500):
                win.blit(again_text,(225,507))
                pygame.draw.rect(win,(100,100,100),(200,500,150,50))
                win.blit(again_text,(225,507))
                if click[0]==1:
                    game_loop()
            else:
                win.blit(again_text,(225,507))
                pygame.draw.rect(win,(0,0,0),(200,500,150,50))
                win.blit(again_text,(225,507))

            if(400+150>mouse[0]>400 and 500+50>mouse[1]>500):
                win.blit(quit_text,(437,507))
                pygame.draw.rect(win,(100,100,100),(400,500,150,50))
                win.blit(quit_text,(437,507))
                if click[0]==1:
                    pygame.quit()
            else:
                win.blit(quit_text,(437,507))
                pygame.draw.rect(win,(0,0,0),(400,500,150,50))
                win.blit(quit_text,(437,507))

            pygame.display.update()
            clock.tick(15)
        

def redrawWindow():
    largeFont = pygame.font.Font('C:\Windows\Fonts\Bahnschrift.ttf',30) #폰트 오브젝트
    win.blit(bg,(bgX,0))
    win.blit(bg,(bgX2,0))

    text = largeFont.render('Score: '+str(score),True,(255,255,255),(0,0,0))
    runner.draw(win)

    win.blit(text,(50,40))
    for i in range(len(heartlist)):
        heartlist[i].draw(win)
    pygame.display.update()

def redrawpooandclover(): 
    for i in range(len(poolist)):
        poolist[i].draw(win)
        if poolist[i].x <=140:
            poolist[i].x = 730
        if poolist[i]. y <= 0 or poolist[i].y >=600:
            poolist[i].y=random.randint(0,570)
            
    for i in range(len(cloverlist)):
        cloverlist[i].draw(win)
        if cloverlist[i].x <=0:
            cloverlist[i].x =700
        if cloverlist[i]. y <= 0 or cloverlist[i].y >=600:
            cloverlist[i].y=random.randint(0,570)

    pygame.display.update()


pygame.time.set_timer(USEREVENT+1,300) # sets the timer for 05 seconds
runner = player(200,470,64,64)
poolist=[]
cloverlist=[]
heartlist=[]
heartlist2=[]

for i in range(12):
    poolist.append(poo(700,random.randint(0,560),24,24))
        
for j in range(5):
    cloverlist.append(clover(700,random.randint(0,570),24,24))

# heartlist.append(heart(600,40,24,24))
# heartlist.append(heart(660,40,24,24))
# heartlist.append(heart(720,40,24,24))

def game_intro():
    dragon = pygame.image.load('Bigdragon.png')
    intro =True

    while intro:
        for event in pygame.event.get():
    #         if event.type== pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #         if event.type== pygame.MOUSEBUTTONDOWN:
    #                 intro=False
    #                 game_loop()

            win.fill((255,216,209))
            win.blit(dragon,(300,220))
            largeFont = pygame.font.SysFont('C:\Windows\Fonts\Bahnschrift.ttf',120)
            largeFont2 = pygame.font.SysFont('C:\Windows\Fonts\Bahnschrift.ttf',80)
            game_name= largeFont.render('Day&Night',True,(0,0,0))
            start_text = largeFont2.render('Start',True,(255,255,255))
            quit_text = largeFont2.render('Quit',True,(255,255,255))

            win.blit(game_name,(200,70))
        # win.blit(quit_text,(200,400))
        # win.blit(start_text,(450,400))
       
            mouse=pygame.mouse.get_pos()
        #print(mouse)
            click= pygame.mouse.get_pressed() #(0,0,0) (1,0,0)
        #print(click)

            if 200+150 >mouse[0]>200 and 500+70 > mouse[1] >500:
                win.blit(quit_text,(213,507))
                pygame.draw.rect(win, (100,100,100), (200,500,150,70))
                win.blit(quit_text,(213,507))
                if click[0]==1:
                    pygame.quit()

            else:
                win.blit(quit_text,(213,507))
                pygame.draw.rect(win,(0,0,0),(200,500,150,70))
                win.blit(quit_text,(213,507))

            if 450+150 >mouse[0]>450 and 500+70 >mouse[1]>500:
                win.blit(start_text,(461,507))
                pygame.draw.rect(win,(100,100,100),(450,500,150,70))
                win.blit(start_text,(461,507))
                if click[0]==1:
                    game_loop()
            else:
                win.blit(start_text,(461,507))
                pygame.draw.rect(win,(0,0,0),(450,500,150,70))
                win.blit(start_text,(461,507))
        pygame.display.update()
        clock.tick(15)

def game_loop():
#Game Loop
    
    run = True
    speed =30
    global score
    bgX=0
    bgX2=bg.get_width()
    heartlist.append(heart(600,40,24,24))
    heartlist.append(heart(660,40,24,24))
    heartlist.append(heart(720,40,24,24))
    

    while run:
    
        if(len(heartlist) == 0):
            run=False
            endScreen()
        score = speed//10-3

        for poo in poolist:
            if poo.collide(runner.hitbox):
                poo.x=0
                runner.falling=True
                pygame.mixer.Sound.play(poo_collision_sound)
                heartlist.pop()
              

        for clover in cloverlist:
            if clover.collide(runner.hitbox):
                clover.x=0
                pygame.mixer.Sound.play(clover_collision_sound)
                if(len(heartlist)==3):
                    pass
                elif(len(heartlist)==2):
                    heartlist.append(heart(720,40,24,24))
                elif(len(heartlist)==1):
                    heartlist.append(heart(660,40,24,24))
                elif(len(heartlist)==0):
                    heartlist.append(heart(600,40,24,24))
        score=speed//5-6
        bgX -= 1.4
        bgX2 -=1.4
        
        if bgX < bg.get_width() * -1: 
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                #quit()
            if event.type == USEREVENT+1:
                speed+=1
            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            pygame.mixer.Sound.play(move_sound)
            runner.up = True
        if keys[pygame.K_DOWN]:
            pygame.mixer.Sound.play(move_sound)
            runner.down =True

        clock.tick(speed)
        redrawWindow()
        redrawpooandclover()

game_intro()