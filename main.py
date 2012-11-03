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
lower = {}
upper = {}

allSprites = pygame.sprite.Group()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
active = pygame.sprite.Group()
background = None

hero = Hero()
active.add(hero)
hero.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

loadedBlocks = set()

static = RelativeSprite(hero)
static.image = load_image('static.png', (40,40))
active.add(static)
static.rect.topleft = (500,400)

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
	changes = active.draw(screen)
	pygame.display.update(changes)
	pygame.display.flip()

def generateTiles(block):
	return pygame.sprite.Group(), pygame.sprite.Group()

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
		toDeLoad = loadedBlocks - shouldBeVisible
		for b in toLoad:
			lower[b], upper[b] = generateTiles(b)
			active.add(lower[b], upper[b])
		for b in toDeLoad:
			lower[b].empty()
			upper[b].empty()
			del lower[b]
			del upper[b]
			active.remove(lower[b], upper[b])
		loadedBlocks = shouldBeVisible
	hero.face(pygame.mouse.get_pos())
	refreshScreen()