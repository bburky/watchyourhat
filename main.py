import pygame
import sys
import math
from Config import Config
from collections import defaultdict
from Hero import Hero
from RelativeSprite import RelativeSprite
from helpers import *
from pygame.locals import *


BG_COLOR = 0,255,255
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

keys = defaultdict(lambda: False)

pygame.init()


# set up sprite groups
seeds = {}
lower = defaultdict(pygame.sprite.Group)
actors = pygame.sprite.Group()
upper = defaultdict(pygame.sprite.Group)
active = pygame.sprite.Group()
loadedBlocks = set()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = None

hero = Hero()
active.add(hero)
actors.add(hero)
hero.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

clock = pygame.time.Clock()

def handleEvents(events):
	for e in events:
		if e.type == KEYDOWN:
			keys[e.key] = True
			if e.key == K_ESCAPE:
				pygame.quit()
		elif e.type == KEYUP:
			keys[e.key] = False
		if e.type == QUIT:
			pygame.quit()
			sys.exit(0)

def whichBlock(pos):
	# calculates the block that the position is part of
	pxPerBlock = Config['PIXELS_PER_TILE']*Config['TILES_PER_BLOCK']
	return (math.floor(pos[0] / pxPerBlock),
		    math.floor(pos[1] / pxPerBlock)
		)

def visibleBlocks(pos):
	# calculates the blocks that should be visible
	(x,y) = map(int, whichBlock(pos))
	return set([(x-1,y-1),
	        (x-1,y+0),
	        (x-1,y+1),
	        (x+0,y-1),
	        (x+0,y+0),
	        (x+0,y+1),
	        (x+1,y-1),
	        (x+1,y+0),
	        (x+1,y+1)
	       ])

def refreshScreen():
	screen.fill(BG_COLOR)
	for l in lower:
		lower[l].draw(screen)
	actors.draw(screen)
	for u in upper:
		upper[u].draw(screen)
	pygame.display.flip()

def generateTiles(block):
	square = pygame.Surface((200,300))
	square.fill((255,0,255))
	sp = RelativeSprite(camera=hero)
	sp.image = square
	sp.rect = square.get_rect()
	sp.truePos = [block[0]*Config['PIXELS_PER_BLOCK']+3, block[1]*Config['PIXELS_PER_BLOCK']]
	return pygame.sprite.Group(sp), pygame.sprite.Group()

def unloadBlock(b):
	lower[b].empty()
	upper[b].empty()
	del lower[b], upper[b]
	active.remove(lower[b], upper[b])

while True:
	dT = clock.tick(60)
	handleEvents(pygame.event.get())
	active.update(dT)
	if keys[K_w]:
		hero.truePos[1] += -hero.speed*dT/1000
	if keys[K_s]:
		hero.truePos[1] += hero.speed*dT/1000
	if keys[K_a]:
		hero.truePos[0] += -hero.speed*dT/1000
	if keys[K_d]:
		hero.truePos[0] += hero.speed*dT/1000

	shouldBeVisible = visibleBlocks(hero.truePos)
	if shouldBeVisible != loadedBlocks:
		toLoad = shouldBeVisible - loadedBlocks
		toUnload = loadedBlocks - shouldBeVisible
		print "Loading", toLoad
		print "Unloading", toUnload
		for b in toLoad:
			lower[b], upper[b] = generateTiles(b)
			active.add(lower[b], upper[b])
		for b in toUnload:
			unloadBlock(b)
		loadedBlocks = shouldBeVisible
	hero.face(pygame.mouse.get_pos())
	refreshScreen()