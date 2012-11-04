import pygame
from helpers import *

class RelativeSprite(pygame.sprite.Sprite):
    def __init__(self, camera=None, offset=None):
        pygame.sprite.Sprite.__init__(self)
        if hasattr(self, 'image'):
            self.rect = self.image.get_rect()

        self.offset = offset
        if not offset:
            self.offset = (0,0)
        self.camera = camera
        self.rect = Rect(-100000,-1000000,1,1)
        self.truePos = self.rect.topleft

    def place(self, (x,y)):
        self.truePos = [x,y]
        self.update()

    def update(self, dT):
        if self.rect and self.camera and self.offset:
            self.rect.x = self.truePos[0] - self.camera.truePos[0] + self.offset[0]
            self.rect.y = self.truePos[1] - self.camera.truePos[1] + self.offset[1]

    def setTruePos(self, pos):
        self.rect.center = pos
        self.update()

    def setCamera(self, cam):
        self.camera = cam

    def setOffset(self, off):
        self.offset = off