import pygame
import math
from RelativeSprite import RelativeSprite
from Config import Config
from helpers import *
from Music import Music

class Hero(pygame.sprite.Sprite):
    images = {}
    speed = 200.0
    maxHealth = 100
    RELOAD_TIME = 2000
    CLIP = 15
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        if not Hero.images:
            ssFoo = Spritesheet('tiles-bottom.png')
            Hero.images['idle'] = ssFoo.image_at(Rect(0*45, 4*45, 45, 45))
            Hero.images['shooting'] = ssFoo.image_at(Rect(0*45, 6*45, 45, 45))
            Hero.images['knife'] = ssFoo.image_at(Rect(7*45, 6*45, 45, 45))
            Hero.images['dead'] = ssFoo.image_at(Rect(13*45, 3*45, 45, 45))
        self.image = Hero.images['shooting']
        self.rect = self.image.get_rect()
        self.speed = Hero.speed
        self.theta = 0.0
        self.truePos = [0,0]
        self.musica = Music()

        self.health = Hero.maxHealth
        self.alive = self.health > 0

        self.ammo = Hero.CLIP

        self.shootTimeout = -1
        self.slashTimeout = -1
        self.reloadTimeout = -1
    
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def shoot(self):
        if self.ammo:
            self.musica.pistolshot()
            self.shootTimeout = 500
            self.image = self.rot_center(Hero.images['shooting'], -90+self.theta)
            self.ammo -= 1
            return True
        else:
            return False

    def reload(self):
        if self.reloadTimeout <= 0:
            self.reloadTimeout = RELOAD_TIME

    def slash(self):
        self.slashTimeout = 200
        self.image = self.rot_center(Hero.images['knife'], -90+self.theta)

    def face(self, pos):
        targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
        if self.slashTimeout > 0:
            imageString = 'knife'
        elif self.shootTimeout > 0:
            imageString = 'shooting'
        else:
            imageString = 'idle'
        self.image = self.rot_center(Hero.images[imageString], -90-targetDir)
        self.theta = -targetDir

    def damage(self, amount):
        self.musica.damaged()
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def update(self, dT):
        if self.shootTimeout > 0:
            self.shootTimeout -= dT
        if self.slashTimeout > 0:
            self.slashTimeout -= dT
        if self.reloadTimeout > 0:
            self.reloadTimeout -= dT
            if self.reloadTimeout <= 0:
                self.ammo = Hero.CLIP
        if self.shootTimeout <= 0 and self.slashTimeout <= 0:
            if self.alive:
                string = 'idle'
            else:
                string = 'dead'
            self.image = self.rot_center(Hero.images[string], -90+self.theta)
