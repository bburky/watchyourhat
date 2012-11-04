import pygame
from pygame.locals import *
from pygame.color import THECOLORS

cache = {}
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, target=None):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.padding = [1,1]
        self.prevPercent = -1
        self.rect = Rect((0,0), (0,0))
        self.image = pygame.Surface(self.rect.size)

    def update(self, dT):
        perc = self.target.health*1.0 / self.target.maxHealth
        if perc == self.prevPercent:
            pass
        else:
            self.prevPercent = perc
            if perc not in cache:
                print "hb cache miss"
                x = 0
                y = 0
                wid = self.target.rect.width
                hei = self.target.rect.height * 0.20
                self.image = pygame.Surface((wid, hei))
                pygame.draw.rect(self.image, (0,0,0), Rect((x, y), (wid, hei)))

                x += self.padding[0]
                wid -= self.padding[0]*2
                y += self.padding[1]
                hei -= self.padding[1]*2
                pygame.draw.rect(self.image, THECOLORS['red'], Rect((x,y), (wid,hei)))

                if perc > 0:
                    wid *= perc
                    pygame.draw.rect(self.image, THECOLORS['green'], Rect((x,y), (wid,hei)))

                cache[perc] = self.image
            self.image = cache[perc]

        self.rect.left = self.target.rect.x
        self.rect.top = self.target.rect.y - self.target.rect.height * 0.20
        self.rect.height = self.target.rect.height * 0.20
        self.rect.width = self.target.rect.width
        if not self.target.alive:
            self.kill()
        if hasattr(self.target, 'aggro') and not self.target.aggro:
            self.rect.size = (0,0)

