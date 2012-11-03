import pygame
import sys
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
sprites = pygame.sprite.Group()
background = None

hero = Hero()
sprites.add(hero)
hero.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

loadedBlocks = set()

static = RelativeSprite(hero)
static.image = load_image('static.png', (40,40))
static.rect = static.image.get_rect()
sprites.add(static)
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

def visibleBlocks(pos):
	# calculates the blocks that should be visible


def refreshScreen():
	screen.fill(BG_COLOR)
	changes = sprites.draw(screen)
	pygame.display.update(changes)
	pygame.display.flip()

while True:
	dT = clock.tick(60)
	sprites.update(dT)
	handleEvents(pygame.event.get())
	if keys[K_w]:
		hero.truePos[1] += -hero.speed*dT/1000
	if keys[K_s]:
		hero.truePos[1] += hero.speed*dT/1000
	if keys[K_a]:
		hero.truePos[0] += -hero.speed*dT/1000
	if keys[K_d]:
		hero.truePos[0] += hero.speed*dT/1000
	hero.face(pygame.mouse.get_pos())
	refreshScreen()