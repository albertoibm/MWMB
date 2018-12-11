import threading
from time import sleep
class Player(threading.Thread):
    """
    player = Player()       # Create object
    player.start()          # Start thread
    player.setTrack(track)  # Set track
    player.play()           # Start playback
    player.pause()          # Pause playback
    player.stop()           # Stop thread
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.piano = None
        self.track = None
        self.preMsg = []
        self.playing = False
        self.running = True
        self._transpose = 0
        self.beatsPerMinute = 160
        self._playOnce = False
    def setPiano(self, p):
        self.piano = p
    def clearTrack(self):
        self.track = None
    def setTrack(self, t):
        #print "Received track with %d messages"%len(t.track)
        self.track = t
        i = 0
        while 1:
            try:
                if self.track.track[i].type != "note_on":
                    self.preMsg.append(self.track.track[i])
                    del(self.track.track[i])
                else:
                    i += 1
            except:
                break
        self.beatsPerMinute = self.track.beatsPerMinute
    def setChannel(self, channel):
        for msg in self.preMsg + self.track.track:
            try:msg.channel = channel
            except:pass
    def getLength(self):
        if self.track != None:
            return self.track.getLength()
        return [None,None,None]
    def run(self):
        self.playing = False
        while self.running:
            while self.playing:
                self._play()
            sleep(0.1)
    def play(self, status = True):
        self.playing = status
    def playOnce(self):
        self._playOnce = True
        self.play()
    def pause(self):
        self.playing = False
    def toggle(self):
        self.playing = bool(1-self.playing)
    def stop(self):
        self.running = False
    def quantize(self,div = 16):
        self.track.quantize(div)
    def transpose(self,arg):
        try:
            if arg.startswith("-") or arg.startswith("+"):
                self._transpose += int(arg)
            else:
                self._transpose = int(arg)
        except ValueError:
            stderr.write("Error. Argumento debe ser entero")
    def speedUp(self,arg):
        self.setSpeed(self.beatsPerMinute+int(arg))
    def speedDown(self,arg):
        self.setSpeed(self.beatsPerMinute-int(arg))
    def setSpeed(self,arg):
        self.beatsPerMinute = int(arg)
    def _play(self):
        if self.piano != None and self.track != None:
            for ctrl in self.preMsg:
                self.piano.sendMsg(ctrl)
            for _msg in self.track.track:
                delay = _msg.time * 60.0 / self.track.ticksPerBeat / self.beatsPerMinute
                sleep(delay)
                if not self.playing:
                    break
                else:
                    msg = _msg.copy()
                    if msg.type == "note_on":
                        msg.note += self._transpose
                    #print msg
                    self.piano.sendMsg(msg)
            if self._playOnce:
                self.playing = False
                self.running = False
                self._playOnce = False
