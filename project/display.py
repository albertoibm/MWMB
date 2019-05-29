from track import Track
from utils import note2char

#from ui import UI

LO = unichr(9603)
HI = unichr(9600)
MD = unichr(9644)

KEYS = 88
MIN = 0
MAX = 88

class Display:
    def __init__(self,ui=None,track=None,width=None,height=None,x=0,y=0):
        self.ui = ui
        if self.ui != None:
            self.height, self.width = map(int,self.ui.size())
        else:
            self.height, self.width = 10,10
        self.cursorY = self.height / 2
        self.cursorX = 44
        self.track = track
        self.bpm = self.track.beatsPerMinute
        self.tpb = self.track.ticksPerBeat
        self.seconds = 60.0 / self.tpb / self.bpm

        #Begin and end using real time
        #self.length = self.track.getLengthInSec()
        #self.begin = 0.0
        #self.end = (self.height-1) * 60.0 / self.bpm
        #self.step = 60.0 / self.bpm
        #Begin and end using beats
        self.length = self.track.getLengthInBeats()
        self.begin = 0
        self.end = self.height-1
        self.step = 1

        self.beats = []
        for i in range(int(self.track.getLengthInBeats()+1)):
            self.beats.append([])
        
        ## Create display window
        if self.width > KEYS:
            displayWidth = KEYS
        else:
            displayWidth = self.width
            MIN = (KEYS - self.width) / 2
            MAX = (KEYS - self.width) / 2 + self.width
        if self.ui != None:
            self.display = self.ui.newWindow(self.height, displayWidth, "display", x, y)
            self.ui.setWindow(self.display)
    def createList(self):
        skip = []
        t = 0.0
        n = 0
        for i in range(len(self.track.track)):
            t += self.track.track[i].time * self.seconds
            if self.track.track[i].type == "note_on":
                if i in skip:
                    skip.remove(i)
                else:
                    msg = self.track.track[i]
                    note = msg.note
                    length = 0
                    j = i + 1
                    ## Find closing msg
                    while j != len(self.track.track):
                        ## accumulate times
                        length += self.track.track[j].time
                        if self.track.track[j].type == "note_on":
                            if self.track.track[j].note == note:
                                ## put on list to skip
                                skip.append(j)
                                break
                        j += 1
                    length *= self.seconds
                    beats = length * self.bpm / 60.0
                    beatZero = int(round(t / 60.0 * self.bpm))
                    for i in range(int(beats+1)):
                        self.beats[beatZero+i].append(note)
        if self.ui == None:
            print "hola"
            for beat in beats:
                print map(beat,note2char)
    ## Display notes with length
    def update(self):
        self.ui.setColorPair(272)
        self.ui.putStrXY(0, self.cursorY, " "*((MAX-MIN)/1))
        self.ui.setColorPair(20)
        self.ui.putStrXY(self.cursorX, self.cursorY, " ")
        for beat in range(self.begin, self.end+1):
            for note in self.beats[beat]:
                y = beat - self.begin
                x = MIN if note < MIN else MAX if note > MAX else note
                x -= MIN
                if self.ui != None:
                    if self.cursorY == y + self.begin and self.cursorX == x:
                        self.ui.setColorPair(272)
                    else:
                        self.ui.setColorPair(262)
                    self.ui.putStrXY(x, y, "o")
        self.ui.refresh()
    def up(self):
        self.cursorY = max(0, self.cursorY-1)
        if self.cursorY < self.height/2 + self.begin:
            self.begin -= self.step
            if self.begin < 0:
                self.begin += self.step
            else:
                self.end -= self.step
    def down(self):
        self.cursorY = min(self.length-1, self.cursorY+1)
        if self.cursorY > self.height/2 + self.begin:
            self.end += self.step
            if self.end > self.length:
                self.end -= self.step
            else:
                self.begin += self.step
    def left(self):
        self.cursorX = max(0, self.cursorX-1)
    def right(self):
        self.cursorX = min(87, self.cursorX+1)
    def pgup(self):
        self.cursorY = max(0, self.cursorY-10)
        self.begin -= self.step * 10
        if self.begin < 0:
            self.begin += self.step * 10
        else:
            self.end -= self.step * 10
    def pgdown(self):
        self.cursorY = min(self.length, self.cursorY+10)
        self.end += self.step * 10
        if self.end > self.length:
            self.end -= self.step * 10
        else:
            self.begin += self.step * 10

