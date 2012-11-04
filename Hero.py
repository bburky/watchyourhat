import pygame
import math
from RelativeSprite import RelativeSprite
from Config import Config
from helpers import *

class Hero(pygame.sprite.Sprite):
	images = {}
	speed = 1000.0
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		if not Hero.images:
			Hero.images['idle'] = load_image('hero.png', (20,20))
		self.image = Hero.images['idle']
		self.rect = self.image.get_rect()
		self.speed = Hero.speed
		self.theta = 0.0
		self.truePos = list(self.rect.center)

	def face(self, pos):
		targetDir = math.degrees(math.atan2(pos[1] - self.rect.centery, pos[0] - self.rect.centerx))
		self.image = pygame.transform.rotate(Hero.images['idle'], -90-targetDir)