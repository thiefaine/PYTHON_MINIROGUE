import sys
import re
import curses
import math
import random

curses.initscr()
class weapon:
    def __init__(self, posx, posy, dmg, name, isOnGround):
        self.posx = posx
        self.posy = posy
        self.dmg = dmg
        self.name = name
        self.isOnGround = isOnGround
    def draw(self):
        if (isOnGround):
            win.addch(self.posy, self.posx, ord('/'), curses.color_pair(2))

class room:
    def __init__(self, posx, posy, width, height):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height

class player:
    def __init__(self, name, pv, posy, posx, gold, weapon):
        self.name = name
        self.pv = pv
        self.posx = posx
        self.posy = posy
        self.gold = gold
        self.weapon = weapon
    def move(self, x, y, m):
        canMove = True
        if (not m[self.posy + y][self.posx + x] == '1' and not m[self.posy + y][self.posx + x] == ' '):
            for e in enemyList:
                if (e.posx == self.posx + x and e.posy == self.posy + y):
                    canMove = False
            if canMove:
                for g in goldList:
                    if (g[1] == self.posy + y and g[0] == self.posx + x):
                        self.gold += 10
                        goldList.remove(g)
                for p in potionList:
                    if (p[1] == self.posy + y and p[0] == self.posx + x):
                        self.pv += 15
                        potionList.remove(p)
                        if self.pv >= 100:
                            self.pv = 100
                self.posx += x
                self.posy += y
    def draw(self):
        win.addch(self.posy, self.posx, curses.ACS_DIAMOND, curses.color_pair(4))
    def attack(self):
        for e in enemyList:
            if(abs(self.posx - e.posx) <= 1 and abs(self.posy - e.posy) <= 1):
                e.pv -= self.weapon.dmg
                if (e.pv <= 0):
                    enemyList.remove(e)

class enemy:
    def __init__(self, pv, x, y, dmg, c=None):
        self.pv = pv
        self.posx = x
        self.posy = y
        self.dmg = dmg
        if c is None:
            self.c = curses.ACS_CKBOARD
        else:
            self.c = c
    def move(self, x, y, m):
        if (m[self.posy + y][self.posx + x] == '2' or m[self.posy + y][self.posx + x] == '9'):
            self.posx += x
            self.posy += y
    def attack(self, p):
        malus = random.randint(1, 6)
        p.pv -= self.dmg - malus
    def draw(self):
        win.addch(self.posy, self.posx, self.c, curses.color_pair(5))
    def find(self, p):
        if (p.posx is not self.posx):
            self.posx += (p.posx - self.posx > 0) and 1 or -1
        elif (p.posy is not self.posy):
            self.posy += (p.posy - self.posy > 0) and 1 or -1
    def update(self, p, m):
        if(abs(self.posx - p.posx) <= 1 and abs(self.posy - p.posy) <= 1):
            self.attack(p)
        elif (m[self.posy][self.posx] == m[p.posy][p.posx]):
            self.find(p)
        else:
            pass

def quitWindow():
    win.clear()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    sys.exit(0)

def drawMap(m):
    for j in range(len(m)):
        for i in range(len(m[j])):
            if (m[j][i] == '1'):
                win.addstr(j, i, " ", curses.color_pair(1))
            elif (m[j][i] == '2'):
                win.addstr(j, i, " ", curses.color_pair(2))

# ========= init window ========= #
stdscr = curses.initscr()
stdscr.immedok(True)

curses.noecho()
curses.cbreak()

curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)
curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_WHITE)
curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_CYAN)

curses.curs_set(0)

oriX, oriY = 0, 0
width, height = 120, 50

win = curses.newwin(height, width, oriY, oriX)
win.clear()
#win.nodelay(True)
win.immedok(True)

hudpad = curses.newpad(10, width)

random.seed()

# ========== Read Map =========== #
mapGame = [line.rstrip('\n') for line in open('map.txt')]

# ========= Create Player ======== #
weap = weapon(0, 0, 20, "Vorpal", False)
pla = player("jean", 100, 3, 3, 0, weap)

# ======== Create Enemies ======== #
e1 = enemy(50, 20, 8, 10)
e2 = enemy(50, 6, 2, 10)
e3 = enemy(80, 67, 15, 14)
e4 = enemy(80, 50, 12, 13)
e5 = enemy(150, 48, 28, 15, curses.ACS_LANTERN)
enemyList = [e1, e2, e3, e4, e5]

# ========= Create Items ========= #
goldList = [[4, 3], [19, 5]]
potionList = [[16, 3], [33, 14], [73, 14], [46, 25]]

# ========== Game update ========= #
drawMap(mapGame)

game = True

while game:
    stdscr.clear()
    drawMap(mapGame)

    pla.draw()
    for e in enemyList:
        e.draw()

    for g in goldList:
        win.addch(g[1], g[0], 'G', curses.color_pair(6))

    for p in potionList:
        win.addch(p[1], p[0], 'P', curses.color_pair(7))

    # ==== HUD === #
    win.addstr(height - 20, 2, "PV : " + str(pla.pv), curses.color_pair(3))
    win.addstr(height - 20, 30, "Name : " + str(pla.name), curses.color_pair(3))
    win.addstr(height - 20, 50, "Gold : " + str(pla.gold), curses.color_pair(3))
    win.addstr(height - 18, 2, "Weapon : " + str(pla.weapon.name), curses.color_pair(3))
    win.addstr(height - 18, 30, "Dmg : " + str(pla.weapon.dmg), curses.color_pair(3))

    # === LEGENDS === #

    win.addch(height - 16, 1, curses.ACS_LANTERN, curses.color_pair(5))
    win.addstr(height - 16, 3, " : Boss")
    win.addch(height - 15, 1, curses.ACS_CKBOARD, curses.color_pair(5))
    win.addstr(height - 15, 3, " : Enemy")
    win.addch(height - 14, 1, curses.ACS_DIAMOND, curses.color_pair(4))
    win.addstr(height - 14, 3, " : Hero")
    win.addch(height - 13, 1, 'G', curses.color_pair(6))
    win.addstr(height - 13, 3, " : Gold")
    win.addch(height - 12, 1, 'P', curses.color_pair(7))
    win.addstr(height - 12, 3, " : Potion")

    k = stdscr.getch()
    if (k == ord('w')):
        pla.move(0,-1, mapGame)
    elif (k == ord('a')):
        pla.move(-1,0, mapGame)
    elif (k == ord('d')):
        pla.move(1,0, mapGame)
    elif (k == ord('s')):
        pla.move(0,1, mapGame)
    elif (k == ord(' ')):
        pla.attack()
    elif (k == ord('q')):
        quitWindow()
    else:
        pass

    for el in enemyList:
        el.update(pla, mapGame)

    if (pla.pv <= 0):
        game = False
        victory = False
    if len(enemyList) == 0:
        game = False
        victory = True

# ===== End Screen ==== #

win.clear()
win.box()
if victory:
    win.addstr(height / 2, width / 2, "Victory", curses.color_pair(2))
else:
    win.addstr(height / 2, width / 2, "Game Over", curses.color_pair(2))
while (stdscr.getch() is not ord('q')):
    pass
quitWindow()
