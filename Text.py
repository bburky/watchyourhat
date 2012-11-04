

import pygame
import textwrap
from helpers import render_textrect

class Text(pygame.sprite.Sprite):
    def __init__(self, st):
        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.st = st
        self.color = (0,0,0)
        self.size = 32
        self.rect = None
        self.font = None
        self.bgColor = (255,255,255,255)
        self.maxArea = None
        self.justification = 0
        
        #CALL THIS LAST
        self.createImage()
    
    def createImage(self):
        if self.font:
            f = self.font
        else:
            f = pygame.font.get_default_font()
        
        if self.maxArea:
            r = self.maxArea
        else:
            r = pygame.Rect(0,0,1000, 1000)
        
        if self.rect:
            pos = self.rect.topleft
        else:
            pos = None
        self.image = render_textrect(self.st, pygame.font.Font(self.font, self.size), r, self.color, self.bgColor, self.justification)
        self.rect = self.image.get_rect()
        if pos is not None:
            self.rect.topleft = pos

    def setText(self, value):
        self.st = value
        self.createImage()
    def getText(self):
        return self.st
    def delText(self):
        del self.st

    string = text = property(getText, setText, delText, "")