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
from Item import *
from RelativeSprite import RelativeSprite
from Helicopter import Helicopter
from Text import Text
from HealthBar import HealthBar
from Music import Music
import time
import multiplayer
import threading

# Sterling's tired. This is his network code. Sorry.

hero = None

all_generated = False

enemies_list = {}
enemies_list_lock = threading.Lock()
block_lock = threading.Lock()
enemies_n = 1

def manage_network():
    global hero
    while not all_generated: time.sleep(.5)
    
    allies2 = {}
    my_id = -1
    if multiplayer.hosting:
        my_id = 0
        allies2[my_id] = hero
    
    enemy_update_time = time.time()
    while True:
        
        # Send position updates
        x, y = hero.truePos
        theta = hero.theta
        if my_id > -1:
            multiplayer.s.send('1 %d %d %d %d;' % (my_id, x, y, theta))

        if multiplayer.hosting:
            for i in multiplayer.pos:
                x, y, theta = multiplayer.pos[i]
                multiplayer.s.send('1 %d %d %d %d;' % (i, x, y, theta))
            
            #print len(enemies_list)
            if time.time() - enemy_update_time > 1:
                enemy_update_time = time.time()
                enemies_list_lock.acquire()
                for i in enemies_list:
                    en = enemies_list[i]
                    x, y = en.truePos
                    #tgt = en.target.n
                    multiplayer.s.send('2 1 %d %d %d 0;' % (i, x, y))
                enemies_list_lock.release()

        # Harvest Messages
        multiplayer.msg_lock.acquire()

        for m in multiplayer.msg_buff:
            #print "harvesting message: %s" % m
            m = m.split(' ')
            m_t = int(m[0])

            if m_t == 0:
                my_id = int(m[1])
                allies2[my_id] = hero
            elif m_t == 1:
                if len(multiplayer.msg_buff) > 500: continue
                i = int(m[1])
                if i == my_id or my_id == -1: continue
                
                if i not in multiplayer.pos:
                    allies2[i] = addAlly()
                    allies2[i].n = i
                    print "New player rendered"
                    if multiplayer.hosting:
                        for b in upper:
                            new_m = '3 %d %d %d;' % (b[0], b[1], seeds[b])
                            multiplayer.s.send(new_m)
                multiplayer.pos[i] = tuple(int(j) for j in m[2:])
                allies2[i].truePos = list(multiplayer.pos[i][:2])
                allies2[i].theta = multiplayer.pos[i][2]
            elif m_t == 2:
                if len(multiplayer.msg_buff) > 500: continue
                en_t = int(m[1])
                
                i, x, y, tgt = [int(i) for i in m[2:]]
                
                enemies_list_lock.acquire()
                if i not in enemies_list:
                    dx, dy = mapgen.tiles[1][0]
                    wid = hei = Config['PIXELS_PER_TILE']
                    rec = Rect((dx*wid, dy*hei), (wid, hei))
                    img = ssTop.image_at(rec)
        
                    #truePos = [block[0]*Config['PIXELS_PER_BLOCK']+e[0]*45, block[1]*Config['PIXELS_PER_BLOCK']+e[1]*45]
                    truePos = [x, y]
                    spr = ethunterone(*truePos)
                    spr.setCamera(hero)
                    spr.setOffset((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    spr.update(0)
                    enemies.add(spr)
                    actors.add(spr)
                    active.add(spr)
                    spr.target = hero
                    spr.n = i
                    
                    middle[(0,0)].add(spr)
                    #gpEnem.add(spr)
                    
                    hb = HealthBar(target=spr)
                    actors.add(hb)
                    active.add(hb)
                    
                    spr.clientUpdate = True
                    enemies_list[i] = spr
                
                spr.target = allies2[tgt]
                enemies_list[i].truePos = [x, y]
                enemies_list_lock.release()
            elif m_t == 3:
                x, y, sd = [int(i) for i in m[1:]]
                if (x, y) in lower: continue
                seeds[(x, y)] = sd
                loadBlock((x, y))
            elif m_t == 4:
                x, y = [int(i) for i in m[1:]]
                if (x, y) not in lower: continue
                unloadBlock((x, y))
            elif m_t == 5:
                i, dmg = [int(i) for i in m[1:]]
                if i not in enemies_list[i]: continue
                block_lock.acquire()
                enemies_list[i].damage(dmg)
                block_lock.release()
            elif m_t == 6:
                block_lock.acquire()
                i, dmg = [int(i) for i in m[1:]]
                allies2[i].damage(dmg)
                block_lock.release()
        del multiplayer.msg_buff[:]
        multiplayer.msg_lock.release()
        
        time.sleep(.05)

multi_args = 1
if '--fullscreen' in sys.argv: multi_args += 1

if len(sys.argv) <= multi_args:
    multiplayer.init_network()
else:
    multiplayer.init_network(sys.argv[-1])
threading.Thread(target=manage_network).start()
# End of this selection of Sterling's bad choices.

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

keys = defaultdict(lambda: False)
buttons = defaultdict(lambda: False)

pygame.init()
musica = Music()
##musica.junglestart()
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
items = pygame.sprite.Group()
lines = set()
loadedBlocks = set()

#sprite sheets
ssBottom = Spritesheet('tiles-bottom.png')
ssTop = Spritesheet('tiles-top.png')
background = None

#some state
random.seed(time.time())

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

gameover = pygame.sprite.Sprite()
gameover.image = load_image('gameover.png')
gameover.rect = gameover.image.get_rect()
gameover.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
musica.gameover()

gem = pygame.sprite.Sprite()
gem.image = ssBottom.image_at(Rect(1*45, 3*45, 45, 45))
gem.rect = gem.image.get_rect()
gem.rect.topleft = (0, SCREEN_HEIGHT-45*2)

moneyText = Text("0")
moneyText.color = (255, 0, 0)
moneyText.bgColor = (0,0,0,0)
moneyText.rect.topleft = Vec2d(gem.rect.topright) + Vec2d(5, 18)
moneyText.createImage()

bullets = pygame.sprite.Sprite()
bullets.image = ssBottom.image_at(Rect(8*45, 6*45, 45, 45))
bullets.rect = bullets.image.get_rect()
bullets.rect.right -= 100
bullets.rect.topleft = (0, SCREEN_HEIGHT-45)

bulletsText = Text(str(hero.ammo))
bulletsText.color = (255, 0, 0)
bulletsText.bgColor = (0,0,0,0)
bulletsText.rect.topleft = Vec2d(bullets.rect.topright) + Vec2d(5, 18)
bulletsText.createImage()

clock = pygame.time.Clock()

all_generated = True

def handleEvents(events):
    for e in events:
        if e.type == KEYDOWN:
            keys[e.key] = True
            if e.key == K_ESCAPE:
                pygame.quit()
        if e.type == KEYDOWN and e.key == K_e:
            for i in items:
                if i.rect.colliderect(hero.rect):
                    i.kill()
                    moneyText.string = str(int(moneyText.string) + 1)
                    moneyText.createImage()
                    break
        elif e.type == KEYDOWN and e.key == K_r:
            hero.reload()
            musica.pistolreload()
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
            musica.knife()

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
    block_lock.acquire()

    if hero.reloadTimeout >= 0:
        bulletsText.setText("Reloading...")
    else:
        bulletsText.setText(str(hero.ammo))

    screen.fill(Config['BG_COLOR'])
    changes = []
    vis = visibleBlocks(hero.truePos)
    for l in lower:
        if l in vis:
            lower[l].draw(screen)
    if gameStarted:
        actors.draw(screen)
    for l in lines:
        pygame.draw.line(screen, *l)
    lines.clear()
    for u in upper:
        if u in vis:
            upper[u].draw(screen)
    gui.draw(screen)
    pygame.display.flip()
    block_lock.release()

def generateTiles(block):
    global enemies_n
    gpBack = pygame.sprite.RenderUpdates()
    gpFore = pygame.sprite.RenderUpdates()
    gpEnem = pygame.sprite.RenderUpdates()

    prevGenerated = True
    if block not in seeds:
        prevGenerated = False
        seeds[block] = random.randrange(0,10000000)

    bg, fg, en, it = mapgen.gen_block(seeds[block])
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

    if not prevGenerated and multiplayer.hosting:
        for e in en:
            x, y = mapgen.tiles[en[e]][0]
            wid = hei = Config['PIXELS_PER_TILE']
            rec = Rect((x*wid, y*hei), (wid, hei))
            img = ssTop.image_at(rec)

            truePos = [block[0]*Config['PIXELS_PER_BLOCK']+e[0]*45, block[1]*Config['PIXELS_PER_BLOCK']+e[1]*45]

            enemyClasses = {1: ethunterone, 2: cat}
            spr = enemyClasses[en[e]](*truePos)
            spr.setCamera(hero)
            spr.setOffset((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            spr.update(0)
            enemies.add(spr)
            actors.add(spr)
            active.add(spr)
            spr.target = hero
            gpEnem.add(spr)

            if not isinstance(spr, cat):
                hb = HealthBar(target=spr)
                actors.add(hb)
                active.add(hb)
            
            enemies_list_lock.acquire()
            enemies_list[enemies_n] = spr
            spr.n = enemies_n
            enemies_n += 1
            enemies_list_lock.release()

    for i in it:
        print i, it[i]
        (x, y) = (3, 3)
        wid = hei = Config['PIXELS_PER_TILE']
        rec = Rect((x*wid, y*hei), (wid, hei))
        print rec
        img = ssBottom.image_at(rec)
        truePos = [block[0]*Config['PIXELS_PER_BLOCK']+i[0]*45, block[1]*Config['PIXELS_PER_BLOCK']+i[1]*45]

        spr = Gem()
        spr.truePos = truePos
        spr.setCamera(hero)
        spr.setOffset((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        spr.update(0)
        items.add(spr)
        active.add(spr)
        actors.add(spr)
        gpEnem.add(spr)

    return gpBack, gpFore, gpEnem

def loadBlock(b):
    block_lock.acquire()
    l, u, m = generateTiles(b)
    lower[b], upper[b] = l, u
    if b not in middle: middle[b] = m
    block_lock.release()

def unloadBlock(b):
    block_lock.acquire()
    for s in lower[b]:
        s.kill()
    for s in upper[b]:
        s.kill()
    del lower[b], upper[b]
    block_lock.release()


def addGunshot(pt1, pt2):
    lines.add(((0,0,0), pt1, pt2))
def passable((x, y)):
    block = whichBlock((x, y))
    tiles = middle[block]
    for m in middle:
        if m.rect.left < x < m.rect.right and m.rect.top < y < m.rect.bottom:
            return False
    return True

def shoot():
    global remainingBullets
    if not hero.alive:
        return
    
    if hero.ammo <= 0:
        hero.reload()
        musica.pistolreload()
        return
    else:
        hero.shoot()
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
            tgt = intersecting[0]
            tgt.damage(10)
            if isinstance(tgt, Ally):
                multiplayer.s.send('6 %d %d;' % (tgt.n, 10))
            else:
                multiplayer.s.send('5 %d %d;' % (tgt.n, 10)) 
            lines.add(((0,0,0), start, intersecting[0].rect.center))
        else:
            lines.add(((0,0,0), start, end))
    else:
        lines.add(((0,0,0), start, end))

    if hero.ammo <= 0:
        hero.reload()

def slash():
    if hero.alive:
        hero.slash()
        collisionSprite = pygame.sprite.Sprite()
        collisionSprite.rect = hero.rect.inflate(20, 20)
        collisionSprite.rect.center = hero.rect.center
        collisions = pygame.sprite.spritecollide(collisionSprite, enemies, False)
        collisions += pygame.sprite.spritecollide(collisionSprite, allies, False)
        for c in collisions:
            c.damage(50)
            if isinstance(c, Ally):
                multiplayer.s.send('6 %d %d;' % (c.n, 30))
            else:
                multiplayer.s.send('5 %d %d;' % (c.n, 30) )

def callHeli():
    print "geduda choppa"
    h = Helicopter()
    musica.helicopterstart()
    h.truePos = [hero.truePos[0], hero.truePos[1]]
    h.camera = hero
    h.setOffset((SCREEN_WIDTH/2 - hero.rect.w, SCREEN_HEIGHT/2 - hero.rect.h))
    h.update(0)
    h.target = hero
    active.add(h)
    actors.add(h)
    #TODO STOP HELIIIII!!!!

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
        collidingGems = pygame.sprite.spritecollide(hero, items, False)
        for c in collidingGems:
            c.kill()
            moneyText.string = str(int(moneyText.string) + 1)
        hurters = pygame.sprite.spritecollide(hero, enemies, False)
        for spr in hurters:
            if spr.attackTimeout <= 0 and spr.alive:
                hero.damage(spr.power)
                spr.attackTimeout = 1000
        if hero.alive:
            if keys[K_w]:
                hero.truePos[1] += -hero.speed*dT/1000
            if keys[K_s]:
                hero.truePos[1] += hero.speed*dT/1000
            if keys[K_a]:
                hero.truePos[0] += -hero.speed*dT/1000
            if keys[K_d]:
                hero.truePos[0] += hero.speed*dT/1000
        else:
            gui.add(gameover)

        if buttons[1] and lastShot < pygame.time.get_ticks() - 500:
            shoot()
            lastShot = pygame.time.get_ticks()

        if buttons[2] and (not lastHeli or lastHeli < pygame.time.get_ticks() - 10000):
            print "heli"
            callHeli()
            lastHeli = pygame.time.get_ticks()

        if lastEnemyCreation < pygame.time.get_ticks() - 1000:
            lastEnemyCreation = pygame.time.get_ticks()
        shouldBeVisible = visibleBlocks(hero.truePos)
        if shouldBeVisible != loadedBlocks and (not lastBlockLoad or lastBlockLoad < pygame.time.get_ticks() - 2000):
            toLoad = shouldBeVisible - loadedBlocks
            toUnload = loadedBlocks - shouldBeVisible
            print "Loading", toLoad
            print "Unloading", toUnload
            if multiplayer.hosting:
                for b in toLoad:
                    loadBlock(b)
                    multiplayer.s.send('3 %d %d %d;' % (b[0], b[1], seeds[b]))
                for b in toUnload:
                    unloadBlock(b)
                    multiplayer.s.send('4 %d %d;' % (b[0], b[1]))
            loadedBlocks = shouldBeVisible
            lastBlockLoad = pygame.time.get_ticks()
        hero.face(pygame.mouse.get_pos())

    if titleTimeout <= 0:
        title.kill()
    elif gameStarted:
        titleTimeout -= dT
        title.image.set_alpha(titleTimeout/2000*255)
    elif any(buttons.values()) or any(keys.values()):
        gameStarted = True
        gui.add(gem)
        gui.add(moneyText)
        gui.add(bullets)
        gui.add(bulletsText)

    crosshair.rect.center = pygame.mouse.get_pos()
    refreshScreen()
