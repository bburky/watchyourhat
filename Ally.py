import pygame
import math
from RelativeSprite import RelativeSprite
from Config import Config
from helpers import *

class Ally(RelativeSprite):
    images = {}
    speed = 200.0
    maxHealth = 100
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if not Ally.images:
            ssFoo = Spritesheet('tiles-bottom.png')
            Ally.images['idle'] = ssFoo.image_at(Rect(0*45, 4*45, 45, 45))
            Ally.images['shooting'] = ssFoo.image_at(Rect(0*45, 6*45, 45, 45))
        self.image = Ally.images['idle']
        self.rect = self.image.get_rect()
        self.speed = Ally.speed
        self.theta = 0.0

        self.health = Ally.maxHealth

        self.shootTimeout = -1
        self.slashTimeout = -1
    
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def shoot(self):
        self.shootTimeout = 200
        self.image = self.rot_center(Ally.images['shooting'], -90+self.theta)

    def slash(self):
        self.slashTimeout = 200
        self.image = self.rot_center(Hero.images['knife'], -90+self.theta)

    def setTheta(self, theta):
        self.theta = theta
        self.image = self.rot_center(Ally.images[imageString], -90-theta)

    def face(self, pos):
        targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
        if self.shootTimeout > 0:
            imageString = 'shooting'
        else:
            imageString = 'idle'
        self.image = self.rot_center(Ally.images[imageString], -90-targetDir)
        self.theta = -targetDir

    def damage(self, amount):
        self.health -= amount

    def update(self, dT):
        RelativeSprite.update(self, dT)
        if self.shootTimeout > 0:
            self.shootTimeout -= dT
        if self.slashTimeout > 0:
            self.slashTimeout -= dT
        if self.shootTimeout <= 0 and self.slashTimeout <= 0:
            self.image = self.rot_center(Hero.images['idle'], -90+self.theta)
