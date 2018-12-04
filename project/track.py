from mido import MidiFile,Message
class Track:
    global to_be_taken
    to_be_taken = ['note_on','control_change']#+['program_change']
    def __init__(self,track = None, tpb = 1920, bpm = 120):
        self.ticksPerBeat = tpb
        self.beatsPerMinute = bpm
        self.length = None
        if track == None:
            self.track = [] ## List of messages
        else:
            self.track = track
    def isEmpty(self):
        return self.track == []
    def loadFile(self, filename):
        self.track = [] # Clear track
        midi = MidiFile(filename)
        track = midi.tracks[0]
        try:
            while 1:
                msg = track.pop()
                if msg.type in to_be_taken:
                    self.track.append(msg)
        except IndexError:
            self.track.reverse()
    ## getLength
    def getLength(self):
        return [self.getLengthInSec(),self.getLengthInBeats(),None]
    def getLengthInSec(self):
        try:
            # If length != None
            return 0 + self.length
        except:
            length = self.getLengthInBeats()
            # (60 sec / 1 min) * (1 min / 120 beats)
            self.length = length * 60.0 / self.beatsPerMinute
            return self.length
    def getLengthInBeats(self):
        length = self.getLengthInTicks()
        length = length / self.ticksPerBeat
        return length
    def getLengthInTicks(self):
        length = 0
        for msg in self.track:
            length += msg.time
        return length
    def appendNote(self, note, velocity, time, seconds = False):
        msg = Message("note_on")
        msg.note = note
        msg.velocity = velocity
        ## time (s) * (ticks / beat) * (beats / min) * (1min / 60s)
        msg.time = time if seconds == False else time * self.ticksPerBeat * self.beatsPerMinute / 60
        self.appendMsg(msg)
    def appendMsg(self, msg):
        self.track.append(msg)
    def quantize(self, smallest = 16):
        newTrack = []
        multipleOf = float(self.ticksPerBeat) / smallest
        for _msg in self.track:
            msg = _msg.copy()
            msg.time = int(int(round(msg.time / multipleOf)) * multipleOf)
            newTrack.append(msg)
        self.track = list(newTrack)
    ## scaleToBar
    # scale the track to a number of beats multiple of beats in a bar
    def scaleToBar(self, beats = 4):
        length = self.getLengthInBeats()
        if length == 0:
            return None
        n = float(beats)
        if length > beats:
            while abs(length - n) > (beats / 2):
                n += beats
        k = n / length
        self.scale(k)
    def scale(self, scaleFactor):
        for msg in self.track:
            msg.time = int(msg.time * scaleFactor)
