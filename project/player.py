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
        self.playing = False
        self.running = True
        self._transpose = 0
        self.beatsPerMinute = 160
    def setPiano(self, p):
        self.piano = p
    def setTrack(self, t):
        #print "Received track with %d messages"%len(t.track)
        self.track = t
        self.beatsPerMinute = self.track.beatsPerMinute
    def run(self):
        self.playing = False
        while self.running:
            while self.playing:
                self._play()
            sleep(0.1)
    def play(self, status = True):
        self.playing = status
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
