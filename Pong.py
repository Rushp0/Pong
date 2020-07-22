import pygame
from pygame import *
import random, math

pygame.init()
window = pygame.display.set_mode((700,500))
pygame.display.set_caption("Pong")
FONT = pygame.font.SysFont("timesnewroman", 30)


class Paddle:

    def __init__(self, pos, window):
        self.window = window
        self.x = pos[0]
        self.y = pos[1]
        self.player = pygame.draw.rect(window, (191, 36, 36), (self.x, self.y, 15,90))
        self.points = 0
        self.step = 5

    def move(self, direction):
        if direction == "UP" and self.y>=0:
            self.y-=self.step
        if direction == "DOWN" and self.y<=500-92:
            self.y+=self.step
        self.draw()

    def draw(self):
        self.player = pygame.draw.rect(self.window, (191, 36, 36), (self.x, self.y, 15, 90), 2)

class Ball:
    def __init__(self):
        self.x = int(350)
        self.y = int(250)
        self.player_points = 0
        self.computer_points = 0
        self.ball = pygame.draw.circle(window, (255,255,255), (self.x,self.y), 10, 0)
        self.step = 4
        self.angle = self.get_random_angle()
        self.init_movement()

    def init_movement(self):
        # makes reflections easier to calculate
        if self.angle<0:
            self.angle+=360
        # for collision with player
        if self.ball.colliderect(player1.player):
            self.x+=1
            if 90<=self.angle<=180:
                self.angle = 180-self.angle
            if 180<=self.angle<=270:
                self.angle = 360-(self.angle-180)
        
        if self.ball.colliderect(player2.player):
            self.x-=1
            if 0<=self.angle<=90:
                self.angle = 180-self.angle
            if 270<=self.angle<=360:
                self.angle = (360-self.angle)+180

        if self.angle<0:
            self.angle+=360
        # for collision with top
        if self.y<0:
            if 0<=self.angle<=90:
                self.angle*=-1
            if 90<=self.angle<=180:
                self.angle = (180-self.angle)+180
        
        if self.angle<0:
            self.angle+=360
        # for collision with bottom
        if self.y>500:
            if 180<=self.angle<=270:
                self.angle = (270-self.angle)+90
            if 270<=self.angle<=360:
                self.angle = (360-self.angle)

        self.x+=self.step*math.cos(math.radians(self.angle))
        self.y+=self.step*math.sin(math.radians(self.angle*-1))

    def draw(self, window):
        self.ball = pygame.draw.circle(window, (255,255,255), (int(self.x),int(self.y)), 10, 0)

    def get_random_angle(self):
        side = random.randint(0,1)
        if side:
            return random.randint(2,45)
        else:
            return random.randint(135,225)

def check_points(b):
    if b.x<0:
        player2.points+=1
        b.x, b.y = 350, 250
        b.angle = b.get_random_angle()
        if b.step<8:
            b.step+=1
    elif b.x>700:
        player1.points+=1
        b.x, b.y = 350, 250
        b.angle = b.get_random_angle()
        if b.step<8:
            b.step+=1

player1 = Paddle((1, 0), window) # turple has location of paddle
player2 = Paddle((685, 0), window)
b = Ball()

running = True
while running:
    window.fill((0,0,0))
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        player1.move("UP")
    if keys[K_s]:
        player1.move("DOWN")
    if keys[K_UP]:
        player2.move("UP")
    if keys[K_DOWN]:
        player2.move("DOWN")

    b.init_movement()
    b.draw(window)
    
    player1.draw()
    player2.draw()

    check_points(b)

    player1_score = FONT.render(str(player1.points), 1, (255,255,255))
    player2_score = FONT.render(str(player2.points), 1, (255,255,255))
    p1_rect = player1_score.get_rect(center=(175, 450))
    p2_rect = player2_score.get_rect(center=(525, 450))
    window.blit(player1_score, p1_rect)
    window.blit(player2_score, p2_rect)

    pygame.draw.rect(window, (255,255,255), (345,0,5,500)) # divider rectangle 
    pygame.display.update()

pygame.quit()