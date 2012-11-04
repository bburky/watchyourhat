import pygame
import os
import time

class Music:
    def __init__(self):
        self.sound = pygame.mixer
        self.sound.init()
        self.helicopter = self.sound.Sound('data/helicopter2.wav')
        self.helicopterin = self.sound.Sound('data/helicopterin.wav')
        self.jungle = self.sound.Sound('data/jungle.wav')
        self.underground = self.sound.Sound('data/underground.wav')
        self.hit = self.sound.Sound('data/hit.wav')
        self.enemyhit = self.sound.Sound('data/enemyhit.wav')
        self.growl = self.sound.Sound('data/growl.wav')
        self.cathurt = self.sound.Sound('data/catdmg.wav')
        self.gemp = self.sound.Sound('data/gem.wav')
        self.pistolrel = self.sound.Sound('data/reload.wav')
        if not self.sound: print 'Warning, sound disabled'
    def pistolshot(self):
        pistolshot = self.sound.Sound('data/gunshotshort.wav')
        pistolshot.play(0)
    def helicopterstart(self):
        self.helicopterin.play(0)
        pygame.time.delay(1900)
        self.helicoptercontinue()
    def pistolreload(self):
        self.pistolrel.play(0)
    def helicoptercontinue(self):
        self.helicopter.play(-1)
    def damaged(self):
        self.hit.play(0)
    def gempick(self):
        self.gemp.play(0)
    def enemydamaged(self):
        self.enemyhit.play(0)
    def catgrowl(self):
        self.growl.play(0)
    def helicopterstop(self):
        self.helicopter.fadeout(2000)
    def catdmg(self):
        self.cathurt.play(0)
    def junglestart(self): #starts jungle music stops underground music
        self.underground.fadeout(5000)
        pygame.time.delay(5000)
        self.jungle.play(-1)
    def undergroundstart(self):#starts underground music stops jungle music
        self.jungle.fadeout(5000)
        pygame.time.delay(5000)
        self.underground.play(-1)
    def stopall(self):#stops all music
        self.jungle.fadeout(5000)
        self.underground.fadeout(5000)
#care = Music()
#care.pistolreload()
#pygame.init()
#sound = pygame.mixer
#sound.init()


#temp = sound.Sound('data/gunshotshort.wav')
#temp2 = sound.Sound('data/helicopter.wav')
#temp.play(-1)
#temp2.play(1)
#sound.music.load('data/jungle')
#pygame.mixer.music.play()



