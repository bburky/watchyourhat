import pygame
from pygame.locals import *
from helpers import *
from RelativeSprite import RelativeSprite


class Item(RelativeSprite):

    def __init__(self):
        RelativeSprite.__init__(self)

class Gem(Item):
    def __init__(self):
        Item.__init__(self)

        self.image = Spritesheet('tiles-bottom.png').image_at(Rect(3*45, 3*45, 45, 45))
        self.rect = self.image.get_rect()

    def worth():
        return 100