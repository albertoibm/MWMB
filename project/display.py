from track import Track
from utils import note2char

from netlogger import NetLogger

#from ui import UI

LO = unichr(9603)
HI = unichr(9600)
MD = unichr(9644)

KEYS = 88
MIN = 0
MAX = 88

logger = NetLogger("localhost",8370)
logger.connect()

class Display:
    def __init__(self,ui=None,track=None,width=None,height=None,x=0,y=0):
        self.ui = ui
        # Offset on left side, leaving space for timestamps
        self.offset = len("00:00.000 ")
        if self.ui != None:
            logger.log("Using ui")
            self.height, self.width = map(int,self.ui.size())
            self.width -= self.offset
        else:
            logger.log("Not using ui")
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


        logger.log("Track's length: %.2f beats"%self.length)

        self.beats = []
        for i in range(int(self.track.getLengthInBeats()+1)):
            self.beats.append([])
        logger.log("width = %d"%self.width)
        ## Create display window
        if self.width > KEYS:
            displayWidth = KEYS + self.offset
        else:
            displayWidth = self.width + self.offset
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
            for beat in beats:
                print map(beat,note2char)
    ## Display notes with length
    def putStrXY(self, x, y, txt, colorPair = 272):
        self.ui.setColorPair(colorPair)
        self.ui.putStrXY(self.offset+x, y, txt)
    def update(self):
        self.putStrXY(0, self.cursorY - self.begin, " "*((MAX-MIN)/1))
        self.putStrXY(self.cursorX, self.cursorY - self.begin, "+", 2)
        for beat in range(self.begin, self.end+1):
            for note in self.beats[beat]:
                y = beat - self.begin
                x = MIN if note < MIN else MAX if note > MAX else note
                x -= MIN
                if self.ui != None:
                    color = 262
                    if self.cursorY == y + self.begin and self.cursorX == x:
                        logger.log("update() - beat = %d"%beat)
                        logger.log("update() - cursorY = %d"%self.cursorY)
                        color = 282
                    self.putStrXY(x, y, "o", color)
        self.ui.refresh()
    def enter(self):
        beat = self.cursorY
        note = self.cursorX
        logger.log("enter()")
    def up(self):
        self.cursorY = max(0, self.cursorY-1)
        logger.log("Up. cursorY = %d"%self.cursorY)
        if self.cursorY < self.height/2 + self.begin:
            self.begin -= self.step
            if self.begin < 0:
                self.begin += self.step
            else:
                self.end -= self.step
    def down(self):
        self.cursorY = min(self.length-2, self.cursorY+1)
        logger.log("Down. cursorY = %d"%self.cursorY)
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
        for i in range(10):
            self.up()
    def pgdown(self):
        for i in range(10):
            self.down()
