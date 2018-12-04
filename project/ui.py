import curses
from sys import argv
from time import sleep

class UI:
    def __init__(self):
        self.windows = {}
        self.currentWindow = ""
        ## Initialise curses
        self.stdscr = curses.initscr()
        self.windows[""]=self.stdscr
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        self.attr = curses.A_ATTRIBUTES
        self.lastLog = ""
    def log(self,msg):
        msg = msg.replace("\n"," - ")
        clear = " " * len(self.lastLog)
        self.stdscr.addstr(curses.LINES-1, 0, clear, curses.A_STANDOUT)
        self.stdscr.addstr(curses.LINES-1, 0, msg, curses.A_STANDOUT)
        self.stdscr.refresh()
        self.lastLog = msg
    def startColor(self):
        curses.start_color()
        curses.use_default_colors()
	for i in range(0, curses.COLORS):
	    curses.init_pair(i + 1, i, -1)
    def refresh(self):
        self.windows[self.currentWindow].refresh()
    def clear(self):
        if self.currentWindow != "":
            self.windows[self.currentWindow].clear()
    def fill(self,c=" "):
        height,width = self.windowSize()
        for y in range(height):
            for x in range(width):
                try:
                    self.windows[self.currentWindow].addch(y,x,c,self.attr)
    #                self.refresh()
                except:pass
    def windowSize(self):
        if self.currentWindow == "":
            return self.size()
        else:
            return self.windows[self.currentWindow].getmaxyx()
    def size(self):
        return (curses.LINES, curses.COLS)
    def setBackground(self, c, attr=curses.A_ATTRIBUTES):
        if self.currentWindow != "": # not stdscr
            self.windows[self.currentWindow].bkgdset(c,self.color)
    def setBorderParam(self, param, val):
        pass
    def border(self, n=None):
        if n != None:
            self.windows[self.currentWindow].border(n)
        self.windows[self.currentWindow].border()
    def setCursor(self, x, y):
        self.putStrXY( x, y, "")
    def setColorPair(self, color_pair):
        self.color = curses.color_pair(color_pair)
	self.attr = self.color
    def putStr(self, s):
        self.windows[self.currentWindow].addstr(s, self.attr)
    def putStrXY(self, x, y, s):
        self.windows[self.currentWindow].addstr(y, x, s, self.attr)
    def putStrWin(self,s):
        x, y = self.windowSize()
        y = 0
        for line in s.split('\n'):
            self.putStrXY(0, y, line)
            y += 1
    def getChar(self):
        return self.stdscr.getch()
    def setWindow(self,win):
        if win in self.windows:
            self.currentWindow = win
            self.stdscr.addstr(curses.LINES-1,0,"\b"*20+"<"+self.currentWindow+">",self.attr)
            return 0
        return -1 #Does not exist
    def newWindow(self, height, width, name="win",x=0, y=0):
        if name in self.windows:
            i = 0
            while 1:
                newname = "{}{}".format(name,i)
                if newname not in self.windows:
                    break
                i += 1
        else:
            newname = name
        self.windows[newname] = curses.newwin(height, width, y, x)
        return newname
    def quit(self, msg=""):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        print msg
        exit()
