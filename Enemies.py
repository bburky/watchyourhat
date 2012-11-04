import pygame
from Config import Config
from helpers import *
import math
from RelativeSprite import RelativeSprite
class ethunterone(RelativeSprite):
    """ Hostile Enemy Hunter Class """
    images = {}
    def __init__(self, x, y):
        RelativeSprite.__init__(self)
        #self.tilewidth = tilewidth
        self.health = 30
        self.aware = Config['PIXELS_PER_TILE']*20
        #self.id = id
        self.speed = 3
        if not ethunterone.images:
            ss = Spritesheet('tiles-bottom.png')
            ethunterone.images['idle'] = ss.image_at(Rect(0*45, 5*45, 45, 45))
            ethunterone.images['dead'] = ss.image_at(Rect(1*45, 5*45, 45, 45))
        self.image = ethunterone.images['idle']
        self.rect = self.image.get_rect()
        self.truePos = [x, y]
        self.range = 50
        self.target = None
    def attack(self, player):
        self.target = player
        #leave to sterling
    def damage(self, dmg):
        self.health = self.health-dmg
        if self.health <= 0:
            self.die()
    def die(self):
        self.alive = False
        self.deathTime = pygame.time.get_ticks()
        self.image = ethunterone.images['dead']
        return self
    def update(self, dT):
        RelativeSprite.update(self, dT)
        #animate
        if self.alive and self.target:
            vel = Vec2d(self.target.truePos) - Vec2d(self.truePos)
            if vel.length < self.aware:
                vel.length = self.speed
                self.truePos += vel
        else:
            if hasattr(self, 'deathTime') and self.deathTime < pygame.time.get_ticks() - 1000:
                self.kill()

    def move(self, (x,y)):
        self.truePos = [x,y]
        self.update()
    def ai(self):
        min = float("inf");
        player = -1;
        playloclist = main.getplayerlocations() #todo
        for i in playloclist:
            temp = math.sqrt(player[0]**2+player[1]**2)
            player = i
            if emp < min:
                min = temp
                player = i
        if min <= self.range:
            pass
            #attack
        elif min <= self.aware:
            #coord = #call sterling function
            move(self, coord)

        