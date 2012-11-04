import pygame
import math
from RelativeSprite import RelativeSprite
from Config import Config
from helpers import *

class Hero(pygame.sprite.Sprite):
    images = {}
    speed = 500.0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if not Hero.images:
            ssFoo = Spritesheet('tiles-bottom.png')
            Hero.images['idle'] = ssFoo.image_at(Rect(0*45, 4*45, 45, 45))
        self.image = Hero.images['idle']
        self.rect = self.image.get_rect()
        self.speed = Hero.speed
        self.theta = 0.0
        self.truePos = list(self.rect.center)

        self.image = pygame.Surface((self.image.get_width()*2, self.image.get_height()*2))
        self.image.blit(Hero.images['idle'], (self.image.get_width()/4, self.image.get_height()/4))

    def face(self, pos):
        targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
        targetDir = targetDir+90
        diff = targetDir - self.theta
        self.image = self.rot_center(self.image, diff)
        self.theta = targetDir