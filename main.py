import pygame
from pygame.locals import *
import sys
import math
import random
from collections import defaultdict
from helpers import *
import mapgen
from Ally import Ally
from Config import Config
from Hero import Hero
from Enemies import *
from RelativeSprite import RelativeSprite
from Helicopter import Helicopter
from Text import Text
from HealthBar import HealthBar
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

keys = defaultdict(lambda: False)
buttons = defaultdict(lambda: False)

pygame.init()
flags = pygame.DOUBLEBUF|pygame.SRCALPHA|pygame.HWACCEL
if "--fullscreen" in sys.argv:
    flags |= pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)


# set up sprite groups
seeds = {}
lower = defaultdict(pygame.sprite.RenderUpdates)
middle = defaultdict(pygame.sprite.RenderUpdates)
enemies = pygame.sprite.RenderUpdates()
actors = pygame.sprite.RenderUpdates()
allies = pygame.sprite.RenderUpdates()
upper = defaultdict(pygame.sprite.RenderUpdates)
gui = pygame.sprite.RenderUpdates()
active = pygame.sprite.RenderUpdates()
lines = set()
loadedBlocks = set()

#sprite sheets
ssBottom = Spritesheet('tiles-bottom.png')
ssTop = Spritesheet('tiles-top.png')

background = None

#some state
random.seed(time.time())
remainingBullets = 15

hero = Hero()
active.add(hero)
actors.add(hero)
hero.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
hb = HealthBar(target=hero)
active.add(hb)
actors.add(hb)

fps = Text("")
fps.rect.topleft = (0,0)
fps.maxArea = Rect((0,0), (100, 300))
fps.bgColor = (255,255,255,0)
gui.add(fps)

pygame.mouse.set_visible(False)
crosshair = pygame.sprite.Sprite()
crosshair.image = ssBottom.image_at(Rect(2*45, 3*45, 45, 45))
crosshair.rect = crosshair.image.get_rect()
crosshair.rect.center = pygame.mouse.get_pos()
gui.add(crosshair)

title = pygame.sprite.Sprite()
titleImage = load_image('title.png')
title.image = pygame.Surface(titleImage.get_size(), depth=24)
titleAlphaKey = (0,255,0)
title.image.fill(titleAlphaKey)
title.image.set_colorkey(titleAlphaKey)
title.image.blit(titleImage, (0,0))
title.image.set_alpha(255)
title.rect = title.image.get_rect()
title.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
gui.add(title)

gem = pygame.sprite.Sprite()
gem.image = ssBottom.image_at(Rect(1*45, 3*45, 45, 45))
gem.rect = gem.image.get_rect()
gem.rect.topleft = (0, SCREEN_HEIGHT-45*2)
gui.add(gem)

moneyText = Text("12345")
moneyText.color = (255, 0, 0)
moneyText.bgColor = (0,0,0,0)
moneyText.rect.topleft = Vec2d(gem.rect.topright) + Vec2d(5, 18)
moneyText.createImage()
gui.add(moneyText)

bullets = pygame.sprite.Sprite()
bullets.image = ssBottom.image_at(Rect(8*45, 6*45, 45, 45))
bullets.rect = bullets.image.get_rect()
bullets.rect.right -= 100
bullets.rect.topleft = (0, SCREEN_HEIGHT-45)
gui.add(bullets)

bulletsText = Text(str(remainingBullets))
bulletsText.color = (255, 0, 0)
bulletsText.bgColor = (0,0,0,0)
bulletsText.rect.topleft = Vec2d(bullets.rect.topright) + Vec2d(5, 18)
bulletsText.createImage()
gui.add(bulletsText)

helpText = Text("")
helpText.rect.topleft = (SCREEN_WIDTH-200, 300)
helpText.maxArea = Rect((0,0), (100, 50))
helpText.bgColor = (152,152,152,200)
helpText.string = "Foo"
gui.add(helpText)

clock = pygame.time.Clock()

def handleEvents(events):
    for e in events:
        if e.type == KEYDOWN:
            keys[e.key] = True
            if e.key == K_ESCAPE:
                pygame.quit()
        if e.type == KEYDOWN and e.key == K_e:
            for i in items:
                if i.rect.colliderect(hero.rect):
                    i.pickup()
                    i.kill()
                    moneyText = str(int(moneyText.string) + i.worth())
        elif e.type == KEYUP:
            keys[e.key] = False
        if e.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if e.type == MOUSEBUTTONDOWN:
            buttons[e.button] = True
        if e.type == MOUSEBUTTONUP:
            buttons[e.button] = False

        if e.type == MOUSEBUTTONDOWN and e.button == 3:
            slash()

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
    screen.fill(Config['BG_COLOR'])
    changes = []
    vis = visibleBlocks(hero.truePos)
    for l in lower:
        if l in vis:
            lower[l].draw(screen)
    actors.draw(screen)
    for l in lines:
        pygame.draw.line(screen, *l)
    lines.clear()
    for u in upper:
        if u in vis:
            upper[u].draw(screen)
    gui.draw(screen)
    pygame.display.flip()

def generateTiles(block):
    gpBack = pygame.sprite.RenderUpdates()
    gpFore = pygame.sprite.RenderUpdates()
    gpEnem = pygame.sprite.RenderUpdates()

    prevGenerated = True
    if block not in seeds:
        prevGenerated = False
        seeds[block] = random.random()

    bg, fg, en = mapgen.gen_block(seeds[block])
    for b in bg:
        x, y = mapgen.tiles[bg[b]][0]
        wid = hei = Config['PIXELS_PER_TILE']
        rec = Rect((x*wid, y*hei), (wid, hei))
        img = ssBottom.image_at(rec)
        spr = RelativeSprite(camera=hero, offset=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        spr.image = img
        spr.rect = img.get_rect()
        spr.truePos = [block[0]*Config['PIXELS_PER_BLOCK'] + b[0]*45, block[1]*Config['PIXELS_PER_BLOCK'] + b[1]*45]
        active.add(spr)
        gpBack.add(spr)

    for f in fg:
        x, y = mapgen.tiles[fg[f]][0]
        wid = hei = Config['PIXELS_PER_TILE']
        rec = Rect((x*wid, y*hei), (wid, hei))
        if fg[f] in [1, 10]:
            rec = Rect((x*wid-1, y*hei-0), (wid, hei)) #0, 0 gives transparent image wtf
        img = ssTop.image_at(rec)
        spr = RelativeSprite(camera=hero, offset=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        spr.image = img
        spr.rect = img.get_rect()
        spr.truePos = [block[0]*Config['PIXELS_PER_BLOCK']+f[0]*45, block[1]*Config['PIXELS_PER_BLOCK']+f[1]*45]
        active.add(spr)
        gpFore.add(spr)

    if not prevGenerated:
        for e in en:
            x, y = mapgen.tiles[en[e]][0]
            wid = hei = Config['PIXELS_PER_TILE']
            rec = Rect((x*wid, y*hei), (wid, hei))
            img = ssTop.image_at(rec)

            truePos = [block[0]*Config['PIXELS_PER_BLOCK']+e[0]*45, block[1]*Config['PIXELS_PER_BLOCK']+e[1]*45]
            spr = cat(*truePos)
            spr.setCamera(hero)
            spr.setOffset((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            spr.update(0)
            enemies.add(spr)
            actors.add(spr)
            active.add(spr)
            spr.target = hero
            gpEnem.add(spr)

            hb = HealthBar(target=spr)
            actors.add(hb)
            active.add(hb)

    return gpBack, gpFore, gpEnem

def loadBlock(b):
    l, u, m = generateTiles(b)
    lower[b], upper[b] = l, u
    if b not in middle: middle[b] = m

def unloadBlock(b):
    for s in lower[b]:
        s.kill()
    for s in upper[b]:
        s.kill()
    del lower[b], upper[b]


def addGunshot(pt1, pt2):
    lines.add((0,0,0), pt1, pt2)
def passable((x, y)):
    block = whichBlock((x, y))
    tiles = middle[block]
    for m in middle:
        if m.rect.left < x < m.rect.right and m.rect.top < y < m.rect.bottom:
            return False
    return True

def shoot():
    global remainingBullets
    if not hero.shoot():
        return
    bulletsText.text = str(hero.ammo)
    print hero.ammo
    bulletsText.createImage()
    
    start = hero.rect.center
    delta = Vec2d(1000, 0)
    delta.rotate(-hero.theta)
    end = Vec2d(start) + delta
    intersecting = []
    for e in set(enemies) | set(allies):
        if not e.alive: continue
        offsets = []
        offsets.append(Vec2d(e.rect.topleft) - Vec2d(hero.rect.center))
        offsets.append(Vec2d(e.rect.topright) - Vec2d(hero.rect.center))
        offsets.append(Vec2d(e.rect.bottomleft) - Vec2d(hero.rect.center))
        offsets.append(Vec2d(e.rect.bottomright) - Vec2d(hero.rect.center))
        crosses = [o.cross(delta) for o in offsets]
        if any(c >= 0 for c in crosses) and any(c <= 0 for c in crosses):
            if -45 < delta.angle - (Vec2d(e.rect.center) - Vec2d(hero.rect.center)).angle < 45:
                intersecting.append(e)
    intersecting.sort(key=lambda e: (Vec2d(e.rect.center) - Vec2d(hero.rect.center)).length)
    if intersecting:
        off = Vec2d(intersecting[0].rect.center) - Vec2d(hero.rect.center)
        if off.length < SCREEN_WIDTH:
            intersecting[0].damage(10)
            lines.add(((0,0,0), start, intersecting[0].rect.center))
        else:
            lines.add(((0,0,0), start, end))
    else:
        lines.add(((0,0,0), start, end))
    if not hero.ammo:
        hero.reloadTimeout = Hero.RELOAD_TIME

def slash():
    hero.slash()
    collisions = pygame.sprite.spritecollide(hero, enemies, False)
    collisions += pygame.sprite.spritecollide(hero, allies, False)
    for c in collisions:
        c.damage(30)

def callHeli():
    print "geduda choppa"
    h = Helicopter()
    h.truePos = [hero.truePos[0], hero.truePos[1]]
    h.camera = hero
    h.setOffset((SCREEN_WIDTH/2 - hero.rect.w, SCREEN_HEIGHT/2 - hero.rect.h))
    h.update(0)
    h.target = hero
    active.add(h)
    actors.add(h)

def addAlly():
    a = Ally()
    a.truePos = [hero.truePos[0], hero.truePos[1]]
    a.setCamera(hero)
    a.setOffset((SCREEN_WIDTH/2 - hero.rect.w, SCREEN_HEIGHT/2 - hero.rect.h))
    allies.add(a)
    actors.add(a)
    active.add(a)

    hb = HealthBar(target=a)
    actors.add(hb)
    active.add(hb)
    return a

ally = addAlly()
ally.truePos = [0, 0]
ally.update(0)

lastEnemyCreation = 0
lastBlockLoad = 0
lastShot = -1
lastHeli = 0

gameStarted = False
titleTimeout = 2000.0

while True:
    dT = clock.tick(60)
    fps.string = "%.2f" % (1000.0/dT)
    handleEvents(pygame.event.get())

    if gameStarted:
        active.update(dT)
        if hero.alive:
            if keys[K_w]:
                hero.truePos[1] += -hero.speed*dT/1000
            if keys[K_s]:
                hero.truePos[1] += hero.speed*dT/1000
            if keys[K_a]:
                hero.truePos[0] += -hero.speed*dT/1000
            if keys[K_d]:
                hero.truePos[0] += hero.speed*dT/1000

        if buttons[1] and lastShot < pygame.time.get_ticks() - 500:
            shoot()
            lastShot = pygame.time.get_ticks()

        if buttons[2] and (not lastHeli or lastHeli < pygame.time.get_ticks() - 10000):
            print "heli"
            callHeli()
            lastHeli = pygame.time.get_ticks()

        if pygame.time.get_ticks() > 5000:
            helpText.text = ""
            helpText.bgColor = (152, 152, 152, 0)
        if lastEnemyCreation < pygame.time.get_ticks() - 1000:
            lastEnemyCreation = pygame.time.get_ticks()
        shouldBeVisible = visibleBlocks(hero.truePos)
        if shouldBeVisible != loadedBlocks and (not lastBlockLoad or lastBlockLoad < pygame.time.get_ticks() - 2000):
            toLoad = shouldBeVisible - loadedBlocks
            toUnload = loadedBlocks - shouldBeVisible
            print "Loading", toLoad
            print "Unloading", toUnload
            for b in toLoad:
                loadBlock(b)
            for b in toUnload:
                unloadBlock(b)
            loadedBlocks = shouldBeVisible
            lastBlockLoad = pygame.time.get_ticks()
        hero.face(pygame.mouse.get_pos())

    if titleTimeout <= 0:
        title.kill()
    elif any(buttons.values()):
        gameStarted = True
    elif gameStarted:
        titleTimeout -= dT
        print titleTimeout/2000*255
        title.image.set_alpha(titleTimeout/2000*255)

    crosshair.rect.center = pygame.mouse.get_pos()
    refreshScreen()
