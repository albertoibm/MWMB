from time import time,sleep
from piano.track import Track
class Recorder:
    global to_be_recorded
    to_be_recorded = ['note_on']#,'control_change']#+['program_change']
    def __init__(self,tracks = 1):
        self.piano = None
        self.recording = False
        self.startTime = None
        self.track = []
        self.logger = None
        ## Default: (1920 ticks/beat)(120 beats/min)(1/60 min/sec)
        self.ticksPerBeat = 1920
        self.beatsPerMinute = 120
        self.sec = self.ticksPerBeat * self.beatsPerMinute/ 60.0 # 1*self.sec = 960 ticks
    def handler(self,msg):
        if msg.type in to_be_recorded:
            #do stuff
            if self.recording:
#                print "Recorder::handler() - ",msg
                t = self.timer()
                delay = t*self.sec ## convert to ticks
                msg.time = int(delay)
                self.track.append(msg)
                self.logMsg(msg)
                self.startTime = time()
        else:
            if self.recording:
                msg.time = 0
                self.track.append(msg)
    def setPiano(self, p):
        self.piano = p
        return self.piano.setCallback(self.handler)
    def setLogger(self, logger):
        self.logger = logger
    def logMsg(self, msg):
        if self.logger != None:
            self.logger.log(msg)
    def timer(self):
        return time()-self.startTime
    def record(self):
        if self.piano != None:
            input("To start recording press enter")
            self.startRecording()
            input("To stop recording press enter")
            self.stopRecording()
        else:
            print("Not connected!")
    def startRecording(self):
        if self.piano != None and not self.recording:
            self.recording = True
            self.startTime = time()
            return True
        return False
    def stopRecording(self):
        if self.piano != None and self.recording and self.track != []:
            for msg in self.track:
                msg.time = 0
                if msg.type == "note_on":
                    break
            self.recording = False
            self.startTime = None
    def clear(self):
        self.track = []
    def emit(self):
        return Track(track=self.track,bpm=self.beatsPerMinute,tpb=self.ticksPerBeat)
    def play(self): # Maybe move to player and use change play() to emit()
        if self.piano != None:
            for msg in self.track:
                delay = msg.time * 60.0 / self.ticksPerBeat / self.beatsPerMinute
                sleep(delay)
                self.piano.sendMsg(msg)
        else:
            print("Not connected!")
