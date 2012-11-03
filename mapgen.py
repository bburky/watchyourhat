#!/usr/bin/python
import random


tiles = {}
img_id = 0 # image_id
layer = 1 # -1 = Background | 0 = Collides | 1 = Foreground

# Grass
tiles[0] = [None, -1]

# Tree Trunk
tiles[1] = [None, 0]

# Tree Foilage
tiles[2] = [None, 1]
tiles[3] = [None, 1]
tiles[4] = [None, 1]
tiles[5] = [None, 1]
tiles[6] = [None, 1]
tiles[7] = [None, 1]
tiles[8] = [None, 1]
tiles[9] = [None, 1]

# Helicopter Top Left
tiles[100] = [None, -1]

# Helicopter Clearing
tiles[101] = [None, -1]
tiles[102] = [None, -1]
tiles[103] = [None, -1]
tiles[104] = [None, -1]
tiles[105] = [None, -1]
tiles[106] = [None, -1]
tiles[107] = [None, -1]
tiles[108] = [None, -1]
tiles[109] = [None, -1]

def gen_block(seed):
    sz_x = sz_y = 64
    tr_dens = 10
    random.seed(seed)
    
    mp = [[0] * sz_x for i in xrange(sz_y)]
    blocked = set([])
    
    mp_type = random.sample([0]*100 + [1]*100, 1)[0]
    bg = {}
    fg = {}
    print "-"*8
    print mp_type
    print "-"*8
    
    if mp_type == 1:
        # Generate Clearing
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
        mp[y-2][x-1] = 102
        
        blocked.add((y-2, x+3))
        mp[y-2][x+3] = 104
        
        blocked.add((y+3, x-1))
        mp[y+3][x-1] = 107
        
        blocked.add((y+3, x+3))
        mp[y+3][x+3] = 109
        
        # (Linear Edges)
        top_edge = [(y-2, x-2), (y-3, x), (y-3, x+1), (y-3, x+2), (y-2, x+4)]
        bot_edge = [(y+3, x-2), (y+4, x), (y+4, x+1), (y+4, x+2), (y+3, x+4)]
        left_edge = [(y-1, x-3), (y, x-3), (y+1, x-3), (y+2, x-3)]
        right_edge = [(y-1, x+5), (y, x+5), (y+1, x+5), (y+2, x+5)]
        
        for j, i in top_edge:
            blocked.add((j, i))
            mp[j][i] = 103
    
        for j, i in left_edge:
            blocked.add((j, i))
            mp[j][i] = 105
    
        for j, i in right_edge:
            blocked.add((j, i))
            mp[j][i] = 106
    
        for j, i in bot_edge:
            blocked.add((j, i))
            mp[j][i] = 108
    
    # Generate Trees
    trees = set([])
    while len(trees) < tr_dens:
        x = random.randrange(0, (sz_x - 2) / 3) * 3 + 1
        y = random.randrange(0, (sz_y - 2) / 3) * 3 + 1
        if (y, x) in blocked: continue
        
        trees.add((y, x))
        blocked.add((y, x))
    
    for tr in trees:
        mp[tr[0]][tr[1]] = 1
        fg[(tr[0]-1, tr[1]-1)] = 2
        fg[(tr[0]-1, tr[1])] = 3
        fg[(tr[0]-1, tr[1]+1)] = 4
        fg[(tr[0], tr[1]-1)] = 5
        fg[(tr[0], tr[1]+1)] = 6
        fg[(tr[0]+1, tr[1]-1)] = 7
        fg[(tr[0]+1, tr[1])] = 8
        fg[(tr[0]+1, tr[1]+1)] = 9
    
    
    for j in xrange(sz_y):
        for i in xrange(sz_x):
            bg[(x, y)] = mp[j][i]
    
    print "\n".join("".join(str(i) for i in r) for r in mp)
    return bg, fg

m = gen_block(36731233)

