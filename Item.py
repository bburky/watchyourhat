import pygame
from helpers import *
from pygame.locals import *

class Item(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Gem(Item):
    def __init__(self):
        Item.__init__(self)

        self.image = Spritesheet('tiles-bottom.png').image_at(Rect(10*45, 2*45, 45, 45))
        self.rect = self.image.get_rect()

    def worth():
        return 100