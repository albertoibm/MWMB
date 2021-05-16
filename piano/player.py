import threading
from time import sleep
from piano.utils import note2char
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
        self.verbose = False
        self.n = 0
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
                if self.track.track[i].type not in ["note_on", "control_change"]:
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
    def setN(self, n):
        self.n = n
    def play(self, status = True, verbose = False):
        self.playing = status
        self.verbose = verbose
    def playOnce(self, verbose = False):
        self._playOnce = True
        self.play(verbose=verbose)
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
                    if self.verbose:
                        if msg.type == "note_on" and msg.velocity > 0:
                            print(("{} - {}({}), {}".format(self.n, msg.note,note2char(msg.note),msg.velocity)))
                            self.n += 1
                        elif msg.type == "control_change":
                            print(("{} - ctrl: {}, val: {}".format(self.n, msg.control, msg.value)))
                        #print msg
                    self.piano.sendMsg(msg)
            self.n = 0
            if self._playOnce:
                self.playing = False
                self.running = False
                self._playOnce = False
