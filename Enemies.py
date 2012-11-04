import pygame
from Config import Config
from helpers import *
import math
import random
from RelativeSprite import RelativeSprite
from Music import Music
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
class ethunterone(RelativeSprite):
    """ Hostile Enemy Hunter Class """
    images = {}
    maxHealth = 30
    def __init__(self, x, y):
        RelativeSprite.__init__(self)
        #self.tilewidth = tilewidth
        self.health = ethunterone.maxHealth
        self.aware = Config['PIXELS_PER_TILE']*20
        #self.id = id
        self.speed = 3
        self.musica = Music()
        if not ethunterone.images:
            ss = Spritesheet('tiles-bottom.png')
            ethunterone.images['idle'] = []
            ethunterone.images['idle'].append(ss.image_at(Rect(5*45, 6*45, 45, 45)))
            ethunterone.images['idle'].append(ss.image_at(Rect(6*45, 6*45, 45, 45)))
            ethunterone.images['idle'].append(ss.image_at(Rect(0*45, 5*45, 45, 45)))
            ethunterone.images['dead'] = ss.image_at(Rect(1*45, 5*45, 45, 45))
        self.i = random.choice(range(len(ethunterone.images['idle'])))
        self.image = ethunterone.images['idle'][self.i]
        self.rect = self.image.get_rect()
        self.truePos = [x, y]
        self.range = 50
        self.target = None
    def attack(self, player):
        self.target = player
        #leave to sterling
    def damage(self, dmg):
        self.health = self.health-dmg
        self.musica.enemydamaged()
        if self.health <= 0:
            self.die()
    def die(self):
        self.alive = False
        self.deathTime = pygame.time.get_ticks()
        self.image = ethunterone.images['dead']
        return self
    def update(self, dT):
        RelativeSprite.update(self, dT)

        #change image
        if self.alive:
            if random.random() > 0.7:
                self.i = random.choice(range(len(ethunterone.images['idle'])))
            self.image = ethunterone.images['idle'][self.i]
        else:
            self.image = ethunterone.images['dead']

        #change direction
        if self.target:
            pos = self.target.rect.center
            targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
            self.image = rot_center(self.image, -90-targetDir)

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
        
