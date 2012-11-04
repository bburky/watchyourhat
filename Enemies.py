import pygame
import config
import math
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
		self.range = 50
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
	def move(self, (x,y)):
        self.truePos = [x,y]
        self.update()
	def ai():
	    min = float("inf");
		player = -1;
		playloclist = main.getplayerlocations() #todo
		for i in playloclist:
		    temp = math.sqrt(player[0]**2+player[1]**2)
			player = i
			if emp < min:
			    min = temp
				player = i
		if min <= self.range:
			#attack
		    elif min <= self.aware:
		        #coord = #call sterling function
			    move(self, coord)

		