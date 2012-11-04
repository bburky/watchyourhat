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
class cat(RelativeSprite):
    """Panther Class """
    images = {}
    maxHealth = 50
    attackTimeout = 1000
    power = 10
    def __init__(self, x, y):
        RelativeSprite.__init__(self)
        #self.tilewidth = tilewidth
        self.health = ethunterone.maxHealth
        self.aware = Config['PIXELS_PER_TILE']*3
        #self.id = id
        self.speed = 9
        self.musica = Music()
        if not cat.images:
            ss = Spritesheet('tiles-bottom.png')
            cat.images['idle'] = []
            cat.images['idle'].append(ss.image_at(Rect(12*45, 3*45, 90, 90)))
            cat.images['idle'].append(ss.image_at(Rect(14*45, 3*45, 90, 90)))
            cat.images['dead'] = ss.image_at(Rect(10*45, 3*45, 90, 90))
        self.i = 0
        self.image = cat.images['idle'][self.i]
        self.rect = self.image.get_rect()
        self.truePos = [x, y]
        self.range = 50
        self.target = None
        self.attackTimeout = cat.attackTimeout
        self.aggro = False
    def damage(self, dmg):
        self.health = self.health-dmg
        self.musica.catdmg()
        self.aware = 3000
        if self.health <= 0:
            self.die()
    def die(self):
        self.alive = False
        self.deathTime = pygame.time.get_ticks()
        self.image = cat.images['dead']
        pos = self.target.rect.center
        targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
        self.image = rot_center(self.image, -90-targetDir)
    def update(self, dT):
        RelativeSprite.update(self, dT)
        #change image
        if self.alive:
            self.attackTimeout -= dT
            if random.random() > 0.7:
                self.i = random.choice(range(len(cat.images['idle'])))
            self.image = cat.images['idle'][self.i]
        else:
            self.image = cat.images['dead']

        #change direction
        if self.alive and self.target:
            pos = self.target.rect.center
            targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
            self.image = rot_center(self.image, -targetDir)

        #animate
        if self.alive and self.target:
            vel = Vec2d(self.target.truePos) - Vec2d(self.truePos)
            if vel.length < self.aware:
                self.aggro = True
                vel.length = self.speed
                self.truePos += vel
        else:
            if hasattr(self, 'deathTime') and self.deathTime < pygame.time.get_ticks() - 1000:
                self.kill()
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

class ethunterone(RelativeSprite):
    """ Hostile Enemy Hunter Class """
    images = {}
    maxHealth = 30
    attackTimeout = 1000
    power = 10
    def __init__(self, x, y):
        RelativeSprite.__init__(self)
        #self.tilewidth = tilewidth
        self.health = ethunterone.maxHealth
        self.aware = Config['PIXELS_PER_TILE']*8
        #self.id = id
        self.speed = 3
        self.musica = Music()
        
        self.clientUpdate = False
        
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
        self.attackTimeout = cat.attackTimeout
        
    def damage(self, dmg):
        self.health = self.health-dmg
        self.musica.enemydamaged()
        self.aware = 3000
        if self.health <= 0:
            self.die()
    
    def die(self):
        self.alive = False
        self.deathTime = pygame.time.get_ticks()
        self.image = ethunterone.images['dead']
        pos = self.target.rect.center
        targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
        self.image = rot_center(self.image, -90-targetDir)

    def update(self, dT):
        RelativeSprite.update(self, dT)

        #change image
        if self.alive:
            self.attackTimeout -= dT
            if random.random() > 0.7:
                self.i = random.choice(range(len(ethunterone.images['idle'])))
            self.image = ethunterone.images['idle'][self.i]
        else:
            self.image = ethunterone.images['dead']
        
        #if self.clientUpdate:
        #    targetDir = -self.theta
        #    self.image = rot_center(self.image, -90-targetDir)
        #    return
        
        #change direction
        if self.alive and self.target:
            pos = self.target.rect.center
            targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
            self.image = rot_center(self.image, -90-targetDir)

        #animate
        if self.alive and self.target:
            vel = Vec2d(self.target.truePos) - Vec2d(self.truePos)
            if vel.length < self.aware and vel.length != 0:
                vel.length = self.speed
                self.truePos += vel
        else:
            if hasattr(self, 'deathTime') and self.deathTime < pygame.time.get_ticks() - 1000:
                self.kill()
    
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
        
