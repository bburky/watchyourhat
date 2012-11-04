import pygame
from pygame.locals import *
import sys
import math
import random
from collections import defaultdict
from helpers import *
import mapgen
from Config import Config
from Hero import Hero
from RelativeSprite import RelativeSprite
import time

BG_COLOR = 0,255,255
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

keys = defaultdict(lambda: False)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF|pygame.SRCALPHA)

random.seed(time.time())
# set up sprite groups
seeds = {}
lower = defaultdict(pygame.sprite.RenderUpdates)
middle = defaultdict(pygame.sprite.RenderUpdates)
actors = pygame.sprite.RenderUpdates()
upper = defaultdict(pygame.sprite.RenderUpdates)
active = pygame.sprite.Group()
loadedBlocks = set()

#sprite sheets
ssBottom = Spritesheet('tiles-bottom.png')
ssTop = Spritesheet('tiles-top.png')

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
    changes = []
    for l in lower:
        lower[l].draw(screen)
    actors.draw(screen)
    for u in upper:
        upper[u].draw(screen)
    pygame.display.update(changes)
    pygame.display.flip()

def generateTiles(block):
    gpBack = pygame.sprite.Group()
    gpFore = pygame.sprite.Group()
    gpEnem = pygame.sprite.Group()

    if block not in seeds:
        seeds[block] = random.random()

    bg, fg, en = mapgen.gen_block(seeds[block])
    for b in bg:
        x, y = mapgen.tiles[bg[b]][0]
        wid = hei = Config['PIXELS_PER_TILE']
        rec = Rect((x*wid, y*hei), (wid, hei))
        img = ssBottom.image_at(rec)
        spr = RelativeSprite(camera=hero)
        spr.image = img
        spr.rect = img.get_rect()
        spr.truePos = [block[0]*Config['PIXELS_PER_BLOCK'] + b[0]*45, block[1]*Config['PIXELS_PER_BLOCK'] + b[1]*45]
        active.add(spr)
        gpBack.add(spr)

    for f in fg:
        x, y = mapgen.tiles[fg[f]][0]
        wid = hei = Config['PIXELS_PER_TILE']
        rec = Rect((x*wid, y*hei), (wid, hei))
        if fg[f] == 1:
            rec = Rect((x*wid-1, y*hei-0), (wid, hei)) #0, 0 gives transparent image wtf
        img = ssTop.image_at(rec)
        spr = RelativeSprite(camera=hero)
        spr.image = img
        spr.rect = img.get_rect()
        spr.truePos = [block[0]*Config['PIXELS_PER_BLOCK']+f[0]*45, block[1]*Config['PIXELS_PER_BLOCK']+f[1]*45]
        active.add(spr)
        gpFore.add(spr)

    for e in en:
        x, y = mapgen.tiles[en[e]][0]
        wid = hei = Config['PIXELS_PER_TILE']
        rec = Rect((x*wid, y*hei), (wid, hei))
        img = ssTop.image_at(rec)
        spr = RelativeSprite(camera=hero)
        spr.image = img
        spr.rect = img.get_rect()
        spr.truePos = [block[0]*Config['PIXELS_PER_BLOCK']+e[0]*45, block[1]*Config['PIXELS_PER_BLOCK']+e[1]*45]
        active.add(spr)
        gpEnem.add(spr)

    return gpBack, gpFore, gpEnem

def loadBlock(b):
    lower[b], upper[b], middle[b] = generateTiles(b)

def unloadBlock(b):
    for s in lower[b]:
        s.kill()
    for s in upper[b]:
        s.kill()
    del lower[b], upper[b]

while True:
    dT = clock.tick(60)
    print 1000.0/dT
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
            loadBlock(b)
        for b in toUnload:
            unloadBlock(b)
        loadedBlocks = shouldBeVisible
    hero.face(pygame.mouse.get_pos())
    refreshScreen()
