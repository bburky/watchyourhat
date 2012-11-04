from RelativeSprite import RelativeSprite
from helpers import *
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
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
            if vel.length:
                vel.length = self.speed
            self.truePos += vel
            pos = self.target.rect.center
            targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
            self.image = rot_center(self.image, -90-targetDir)

        self.chFrameTimeout -= dT
        if self.chFrameTimeout <= 0:
            self.chFrameTimeout += Helicopter.change_frame
            self.i += 1
            self.i %= len(Helicopter.frames)
            self.image = Helicopter.frames[self.i]

    def attack(self, entity):
        self.target = entity
