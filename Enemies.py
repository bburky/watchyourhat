import pygame
import config
from RelativeSprite import RelativeSprite
class ethunterone(RelativeSprite):
    """ Hostile Enemy Hunter Class """
    def __init__(self, x, y):
		RelativeSprite.__init__(self):
	    #self.tilewidth = tilewidth
        self.health = 100
		self.aware = config.tilewidth*20
		self.damage = 15
		#self.id = id
		self.speed = config.tilewidth
		self.image = load_image("ethunter1.png")
		self.rect = self.image.get_rect()
		self.truePos = [x, y]
	def attack(playerx, playery):
		#leave to sterling
	def damaged(dmg):
	    self.health = self.health-dmg
		if self.health <= 0:
		    self.die()
	def die():
	    self.damage = 0;
		#TODO
		#animate death
		#remove
		return self
	def update(self, dT):
		#animate
	    RelativeSprite.update(self, dT) #handles move
		