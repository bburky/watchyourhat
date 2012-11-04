from RelativeSprite import RelativeSprite
from helpers import *
class Helicopter(RelativeSprite):
    frames = []
    change_frame = 100
    def __init__(self):
        RelativeSprite.__init__(self)
        if not Helicopter.frames:
            ssHeli = Spritesheet('tiles-bottom.png')
            Helicopter.frames = [ssHeli.image_at(Rect(((10 + 3*i)*45, 0), (45*3, 45*2))) for i in xrange(6)]

        self.speed = 3
        self.chFrameTimeout = Helicopter.change_frame
        self.i = 0
        self.image = Helicopter.frames[self.i]
        self.target = None
        self.rect = self.image.get_rect()

    def update(self, dT):
        RelativeSprite.update(self, dT)
        if self.target:
            vel = Vec2d(self.target.truePos) - Vec2d(self.truePos)
            print self.target.truePos, self.truePos
            if vel.length:
                vel.length = self.speed
            self.truePos += vel
            print self.truePos

        self.chFrameTimeout -= dT
        if self.chFrameTimeout <= 0:
            self.chFrameTimeout += Helicopter.change_frame
            self.i += 1
            self.i %= len(Helicopter.frames)
            self.image = Helicopter.frames[self.i]

    def attack(self, entity):
        self.target = entity