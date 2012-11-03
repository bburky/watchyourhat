#!/usr/bin/env python
from Applejack import Applejack
from Parasprite import Parasprite
from Rainbowdash import Rainbowdash
from Pinkie import Pinkie
from Derpy import Derpy
from Twilight import Twilight
from Rarity import Rarity
from VolumeControl import VolumeControl
from Text import Text
from helpers import *
from pygame.locals import *
from pygame.color import THECOLORS
import os
import pygame
import random
import sys
import menu
import time
import glob
from Generators import PinkiePieGenerator, RainbowdashGenerator,\
	TwilightGenerator, RarityGenerator, DerpyGenerator, ApplejackGenerator

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

Main = 0
class DefenseMain:
	
	def __init__(self, width=1200,height=768):
		pygame.init()
		self.fWidth = width
		self.fHeight = height
		self.pWidth = self.fWidth*3/4
		self.pHeight = self.fHeight
		self.screen = pygame.display.set_mode((self.fWidth, self.fHeight))
		self.sprites = pygame.sprite.RenderUpdates()
		self.towers = pygame.sprite.Group()
		self.clickables = pygame.sprite.Group()
		self.hoverables = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.generators = pygame.sprite.Group()
		self.message = ""
		self.currHover = set()
		self.money = 0
		self.health = 100
		self.background = None
		
		self.towerToPlace = None
		self.gameOver = False

		self.moneyField = Text("")
		
		
		self.enemyPath = [(0.00, 0.10), (0.35, 0.11), (0.37, 0.25), (0.14, 0.45), (0.16, 0.62), (0.28, 0.72), (0.48, 0.70), (0.51, 0.58), (0.47, 0.40), (0.65, 0.11), (0.81, 0.13), (0.78, 0.37), (0.80, 0.68), (0.90, 0.78), (1, 0.78)]
		self.enemyPath = [(x*self.pWidth,y*self.pHeight) for (x,y) in self.enemyPath]
		pygame.mixer.init()
		self.preloadImages()
	
	def quitGame(self):
		pygame.quit()
		sys.exit(0)
	
	def showMessage(self, msg):
		height = 32*len([c for c in msg if c == '\n']) + 128
		scrollImage = load_image('scroll.png', (self.fWidth, height))
		scroll = pygame.sprite.Sprite()
		scroll.image = scrollImage
		scroll.rect = scrollImage.get_rect()
		scroll.rect.bottom = self.fHeight
		
		pygame.font.init()
		f = pygame.font.Font(os.path.join('data', 'fonts', 'ayuma.ttf'), 32)
		textIms = [f.render(m, 1, (0, 0, 0)) for m in msg.split('\n')]
		for i,im in enumerate(textIms):
			scroll.image.blit(im, (100, 25+32*i))
		
		self.screen.blit(scrollImage, scroll.rect)
		pygame.display.flip()

		pygame.event.clear(pygame.USEREVENT)
		pygame.time.set_timer(pygame.USEREVENT, 5000)
		while True:
			ev = pygame.event.wait()
			if ev.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
				break
			elif ev.type == pygame.USEREVENT:
				scroll.kill()
				break
			elif ev.type == pygame.QUIT:
				self.quitGame()
		
		self.refreshScreen(True)
	
	def enemiesWithinRange(self, pt, r):
		targets = [e for e in self.enemies if (Vec2d(pt) - Vec2d(e.rect.center)).get_length() < r and self.screen.get_rect().contains(e.rect)]
		return targets

	def showPonies(self):
		ponyImg = pygame.image.load(os.path.join('data', 'images', 'ponyImg.png'))
		ponyImg = pygame.transform.scale(ponyImg, (self.fWidth, self.fHeight))
		while True:
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					quit()
				if event.type in [MOUSEBUTTONDOWN, KEYDOWN]:
					return
				if event.type == QUIT:
					self.quitGame()
			self.screen.blit(ponyImg, (0,0))
			pygame.display.flip()
	
	def getMoney(self, amt):
		self.setMoney(self.money + amt)
	
	def showMovie(self, fname):
		oldBackground = self.background
		pygame.mixer.quit()
		mov = pygame.movie.Movie(os.path.join('data', 'videos', fname))
		mov.set_display(self.screen, self.screen.get_rect())
		mov.play()
		running = True
		while mov.get_busy() and running:
			for ev in pygame.event.get():
				if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
					running = False
		if mov.get_busy():
			mov.stop()

		self.background = oldBackground

		self.refreshScreen(True)
	
	def playMusic(self, fname, bg=True):
		pygame.mixer.init()
		if bg:
			if fname:
				pygame.mixer.init()
				pygame.mixer.music.load(os.path.join('data', 'audio', fname))
				print "Playing sound track from file %s" % (fname)
				pygame.mixer.music.set_endevent(pygame.USEREVENT)
				pygame.mixer.music.play(-1)
			else:
				pygame.mixer.music.fadeout(500)
		else:
			pygame.mixer.init()
			s = pygame.mixer.Sound(fname)
			print "Playing independed sound from file %s" % fname
			s.play()
	
	def dropdownMenu(self, options):
		self.isPaused = True
		m = menu.Menu()
		m.init(options, self.screen)
		m.set_colors((0,0,0), THECOLORS['black'], (0,0,0))
		m.draw()
		return m.get_selected()
	
	def mainMenu(self):
		self.gameOver = False
		self.screen.blit(load_image('scroll.png', (self.fWidth, self.fHeight)), (0,0))
		self.screen.blit(load_image('logo.png', (400, 500)), (self.fWidth/2 + 100, self.fHeight/2 - 250))
		m = menu.Menu()
		m.init(["Play Game", "Credits", "Quit"], self.screen)
		m.set_colors((0,0,0), THECOLORS['red'], (0,0,0))
		m.draw()
		
		pygame.key.set_repeat(199,69)
		pygame.display.update()
		while True:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_UP:
						m.draw(-1)
					elif event.key == K_DOWN:
						m.draw(1)
					elif event.key == K_RETURN:
						return ["Play Game", "Credits", "Quit"][m.get_position()]
					elif event.key == K_ESCAPE:
						self.quitGame()
				elif event.type == QUIT:
					self.quitGame()
			pygame.time.wait(8)
			pygame.display.flip()
	
	def preloadImages(self):
		'''Attempts to preload all of the images.'''
		os.chdir('data')
		os.chdir('images')
		files = glob.glob('*.png')
		os.chdir('..')
		os.chdir('..')
		for f in files:
			if f != 'logoHiRes.png':
				load_image(f)
	
	def setMoney(self, v):
		self.money = v
		self.moneyField.st = "Money: " + str(self.money)
		self.moneyField.createImage()
	
	def unlock(self, pony):
		for g in self.generators:
			if g.ponyClass == pony:
				g.unlock()
	
	def lockAll(self):
		for g in self.generators:
			g.lock()
	
	def setBackground(self, fname):
		self.background = load_image(fname, (self.fWidth, self.fHeight))
	
	def initializeStatic(self):
		#static elements
		#get volume control going
		self.volControl = VolumeControl(pygame.mixer.music)
		self.volControl.rect.bottomright = (self.fWidth, self.fHeight)
		self.clickables.add(self.volControl)
		self.sprites.add(self.volControl)
		
		clock = pygame.time.Clock()
		
		self.fpsMeter = Text("")
		self.fpsMeter.rect.topleft = (0,0)
		
		self.descField = Text("")
		self.descField.size = 20
		self.descField.rect.topleft = (self.pWidth + 5, 200)
		self.descField.maxArea = pygame.Rect(0, 0, self.fWidth - self.pWidth - 10, 200)
		self.descField.createImage()
		self.sprites.add(self.descField)
		
		self.moneyField = Text("Money: " + str(self.money))
		self.moneyField.maxArea = pygame.Rect(0,0,self.fWidth - self.pWidth - 10, 100)
		self.moneyField.rect.topleft = (self.pWidth + 5, 400)
		self.moneyField.createImage()
		self.sprites.add(self.moneyField)
		self.setMoney(100)

		self.healthField = Text("Health: " + str(self.health))
		self.healthField.maxArea = pygame.Rect(0,0,self.fWidth - self.pWidth - 10, 200)
		self.healthField.rect.topleft = (self.pWidth + 5, self.pHeight*0.8)
		self.healthField.createImage()
		self.sprites.add(self.healthField)


		for i,c in enumerate([PinkiePieGenerator, ApplejackGenerator, TwilightGenerator, RarityGenerator, DerpyGenerator, RainbowdashGenerator]):
			g = c(self)
			g.rect.topleft = (self.pWidth + (i%3)*64, (i/3)*64)
			g.locked = False
			self.sprites.add(g)
			self.clickables.add(g)
			self.hoverables.add(g)
			self.generators.add(g)
			g.updateImages()

	def refreshScreen(self, bg=False):
		if bg and self.background:
			self.screen.blit(self.background, (0,0))
		self.sprites.clear(self.screen, self.background)
		changes = self.sprites.draw(self.screen)
		pygame.display.update(changes)
		pygame.display.flip()
	
	def addEnemy(self, e):
		self.sprites.add(e)
		self.enemies.add(e)
	
	def updateRender(self):
		dTime = pygame.time.wait(10)
		self.fpsMeter.st = "FPS: %f" % (1000.0/dTime)
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.quitGame()
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				if self.towerToPlace and pygame.Rect(0,0,self.pWidth, self.pHeight).collidepoint(event.pos):
					self.sprites.add(self.towerToPlace)
					self.towerToPlace.makeNotGhost()
					self.setMoney(self.money - self.towerToPlace.cost)
					self.towerToPlace = None
				elif self.towerToPlace:
                                        self.towerToPlace.kill()
					self.towerToPlace = None
				for s in self.clickables:
					if s.rect.collidepoint(event.pos):
						s.click()
			elif event.type == MOUSEMOTION:
				if self.towerToPlace:
					self.towerToPlace.rect.center = event.pos
				hovering = set(s for s in self.hoverables if s.rect.collidepoint(event.pos))
				mouseouts = self.currHover - hovering
				mouseovers = hovering - self.currHover
				for s in mouseouts:
					s.unhover()
				for s in mouseovers:
					s.hover()
				self.currHover = hovering
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
                                        if self.towerToPlace:
                                                self.towerToPlace.kill()
                                                self.towerToPlace = None

			if self.health <= 0:
				self.gameOver = True
				print "GAME OVER"
		self.sprites.update(dTime)
		self.refreshScreen(False)
	
	def showCredits(self):
		bg = load_image('cast.png', (self.fWidth, self.fHeight))
		oldbackground = self.background
		self.background = bg
		self.refreshScreen(True)
		self.playMusic('creditsMusic.mp3')
		self.showMessage("Christian Mann\nMark Denhoed\nRoger Mailler\nReddit")

                while True:
                        ev = pygame.event.wait()
                        if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                                break
		self.background = oldbackground
		self.refreshScreen(True)
	def resetState(self):
		self.enemies.empty()
		self.sprites.empty()
		self.towers.empty()
		self.setMoney(100)
		self.health = 100
