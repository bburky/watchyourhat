#!/usr/bin/python
import random
from Config import Config

tiles = {}
img_id = 0 # image_id
layer = 1 # -1 = Background | 0 = Collides | 1 = Foreground

# Grass
tiles[0] = [(5, 4), -1]

# Tree Trunk
tiles[1] = [(2, 1), 0]

# Tree Foilage
tiles[2] = [(1, 0), 1]
tiles[3] = [(2, 0), 1]
tiles[4] = [(3, 0), 1]
tiles[5] = [(1, 1), 1]
tiles[6] = [(3, 1), 1]
tiles[7] = [(1, 2), 1]
tiles[8] = [(2, 2), 1]
tiles[9] = [(3, 2), 1]

# Bush Foilage
tiles[10] = [(1, 4), 1]

# Helicopter Top Left
tiles[100] = [(5, 1), -1]

# Helicopter Clearing
tiles[101] = [(5, 1), -1]

# (dark in center)
tiles[102] = [(4, 3), -1]
tiles[103] = [(5, 3), -1]
tiles[104] = [(6, 3), -1]
tiles[105] = [(4, 4), -1]
tiles[106] = [(6, 4), -1]
tiles[107] = [(4, 5), -1]
tiles[108] = [(5, 5), -1]
tiles[109] = [(6, 5), -1]

# (light in center)
tiles[110] = [(4, 0), -1]
tiles[111] = [(5, 0), -1]
tiles[112] = [(6, 0), -1]
tiles[113] = [(4, 1), -1]
tiles[114] = [(6, 1), -1]
tiles[115] = [(4, 2), -1]
tiles[116] = [(5, 2), -1]
tiles[117] = [(6, 2), -1]

# Ruins tiles
tiles[200] = [(8, 1), -1]

def spawn_room(x, y, max_x, max_y, mp, en, blocked, p=1):
    sz = 5
    if x < 1 or y < 1: return
    if x > max_x - sz + 1 or y > max_y - sz + 1: return
    if (y, x) in blocked: return
    
    for i in xrange(x, x + sz):
        for j in xrange(y, y + sz):
            mp[j][i] = 200
            blocked.add((j, i))
    
    en_c = 0
    while en_c < 3:
        i = random.randrange(x, x + sz)
        j = random.randrange(y, y + sz)
        if (i, j) in en: continue
        
        en_c += 1
        en[(i, j)] = 1
    
    for dx, dy in [(0, -sz), (0, sz), (sz, 0), (-sz, 0)]:
        if random.random() > p: continue
        spawn_room(x+dx, y+dy, max_x, max_y, mp, en, blocked, p*.4)

def gen_block(seed):
    sz_x = sz_y = Config['TILES_PER_BLOCK']
    tr_dens = 0
    bush_dens = 0
    random.seed(seed)
    
    mp = [[0] * sz_x for i in xrange(sz_y)]
    blocked = set([])
    
    mp_type = random.sample([0]*40 + [1]*10 + [2]*15, 1)[0]
    bg = {}
    fg = {}
    en = {}
    
    #print "-"*8
    #print mp_type
    #print "-"*8
    if mp_type == 0:
        tr_dens = 15
        bush_dens = 20
    elif mp_type == 1:
        # Generate Clearing
        tr_dens = 12
        bush_dens = 10
        x = random.randrange(5, (sz_x - 8))
        y = random.randrange(5, (sz_y - 8))
        
        # Center of the clearing
        mp[y][x] = 100
        for j in xrange(y - 1, y + 3):
            for i in xrange(x - 2, x + 5):
                blocked.add((j, i))
                mp[j][i] = 101
            
        for j, i in [(y-2, x), (y-2, x+1), (y-2, x+2), (y+3, x), (y+3, x+1), (y+3, x+2)]:
            blocked.add((j,i))
            mp[j][i] = 101
        
        mp[y][x] = 100
        
        # Edge of the clearing
        # (Diagonal Edges)
        blocked.add((y-2, x-1))
        mp[y-2][x-1] = 109
        blocked.add((y-2, x+3))
        mp[y-2][x+3] = 107
        blocked.add((y+3, x-1))
        mp[y+3][x-1] = 104
        blocked.add((y+3, x+3))
        mp[y+3][x+3] = 102
        
        blocked.add((y-3, x-1))
        mp[y-3][x-1] = 110
        blocked.add((y-3, x+3))
        mp[y-3][x+3] = 112
        blocked.add((y+4, x-1))
        mp[y+4][x-1] = 115
        blocked.add((y+4, x+3))
        mp[y+4][x+3] = 117
        
        blocked.add((y-2, x-3))
        mp[y-2][x-3] = 110
        blocked.add((y-2, x+5))
        mp[y-2][x+5] = 112
        blocked.add((y+3, x-3))
        mp[y+3][x-3] = 115
        blocked.add((y+3, x+5))
        mp[y+3][x+5] = 117
        
        # (Linear Edges)
        top_edge = [(y-2, x-2), (y-3, x), (y-3, x+1), (y-3, x+2), (y-2, x+4)]
        bot_edge = [(y+3, x-2), (y+4, x), (y+4, x+1), (y+4, x+2), (y+3, x+4)]
        left_edge = [(y-1, x-3), (y, x-3), (y+1, x-3), (y+2, x-3)]
        right_edge = [(y-1, x+5), (y, x+5), (y+1, x+5), (y+2, x+5)]
        
        for j, i in top_edge:
            blocked.add((j, i))
            mp[j][i] = 108
    
        for j, i in left_edge:
            blocked.add((j, i))
            mp[j][i] = 106
    
        for j, i in right_edge:
            blocked.add((j, i))
            mp[j][i] = 105
    
        for j, i in bot_edge:
            blocked.add((j, i))
            mp[j][i] = 103
    
    elif mp_type == 2:
        tr_dens = 4
        x = random.randrange(1, sz_x-5-2)
        y = random.randrange(1, sz_y-5-2)
        
        spawn_room(x, y, sz_x-1, sz_y-1, mp, en, blocked)
    
    # Generate Trees
    trees = set([])
    while len(trees) < tr_dens:
        x = random.randrange(0, (sz_x - 2) / 3) * 3 + 1
        y = random.randrange(0, (sz_y - 2) / 3) * 3 + 1
        if (y, x) in blocked: continue
        
        trees.add((y, x))
        for j in xrange(y - 1, y + 2):
            for i in xrange(x - 1, x + 2):
                blocked.add((j, i))
        tr = (j, i)
        
        mp[tr[0]][tr[1]] = 1
        fg[(tr[1], tr[0])] = 1
        fg[(tr[1] - 1, tr[0] - 1)] = 2
        fg[(tr[1], tr[0] - 1)] = 3
        fg[(tr[1] + 1, tr[0] - 1)] = 4
        fg[(tr[1] - 1, tr[0])] = 5
        fg[(tr[1] + 1, tr[0])] = 6
        fg[(tr[1] - 1, tr[0] + 1)] = 7
        fg[(tr[1], tr[0] + 1)] = 8
        fg[(tr[1] + 1, tr[0] + 1)] = 9
        
        if random.random() < .15:
            en[(x, y)] = 2
    

    
    #Generate Bushes
    bush_c = 0
    while bush_c < bush_dens:
        x = random.randrange(0, sz_x)
        y = random.randrange(0, sz_y)
        if (y, x) in blocked: continue
        
        bush_c += 1
        mp[y][x] = 10
        blocked.add((y, x))
    
    for j in xrange(sz_y):
        for i in xrange(sz_x):
            bg[(i, j)] = mp[j][i]
    
    #print "\n".join("".join(str(i) for i in r) for r in mp)
    
    # Generate Enemies
    en_fq = 5
    while len(en) < en_fq:
        x = random.randrange(1, sz_x - 2)
        y = random.randrange(1, sz_y - 2)
        if (x, y) in en or (x, y) in blocked: continue
        
        en[(x,y)] = 1
    
    #print en
    return bg, fg, en

m = gen_block(712)

