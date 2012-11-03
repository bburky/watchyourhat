import pygame
from helpers import *

class RelativeSprite(pygame.sprite.Sprite):
	def __init__(self, camera=None):
		pygame.sprite.Sprite.__init__(self)
		if hasattr(self, 'image'):
			self.rect = self.image.get_rect()
		if not camera:
			camera = [0,0]
		self.camera = camera
		self.truePos = [0,0]

	def place(self, (x,y)):
		self.truePos = [x,y]
		self.update()

	def update(self, dT):
		if self.rect:
			self.rect.x = self.truePos[0] - self.camera.rect.centerx
			self.rect.y = self.truePos[1] - self.camera.rect.centery

	def setTruePos(self, pos):
		self.rect.center = pos
		self.update()

	def setCamera(self, cam):
		self.camera = cam