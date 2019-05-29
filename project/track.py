from mido import MidiFile,Message
PEDAL_ON  = Message(type="control_change",control=64,value=127)
PEDAL_OFF = Message(type="control_change",control=64,value=0)
class Track:
    global to_be_taken
    to_be_taken = ['note_on','control_change']#+['program_change']
    def __init__(self,track = None, tpb = 1920, bpm = 120):
        self.ticksPerBeat = tpb
        self.beatsPerMinute = bpm
        self.length = None
        self.seconds = 60.0 / self.ticksPerBeat / self.beatsPerMinute
        if track == None:
            self.track = [] ## List of messages
        else:
            self.track = track
    def clear(self):
        self.track = []
    def isEmpty(self):
        return self.track == []
    def writeTrackFile(self, filename):
        from utils import note2char
        fopen = open(filename, 'w')
        skip = []
        fopen.write("{}\n".format(self.ticksPerBeat))
        fopen.write("{}\n".format(self.beatsPerMinute))
        fopen.write("{}\n".format(len(self.track)))
        n = 0
        t = 0.0
        for i in range(len(self.track)):
            t += self.track[i].time * self.seconds
            if self.track[i].type == "note_on":
                if i in skip:
                    skip.remove(i)
                else:
                    msg = self.track[i]
                    note = msg.note
                    length = 0#msg.time
                    j = i + 1
                    while j != len(self.track):
                        length += self.track[j].time
                        if self.track[j].type == "note_on":
                            if self.track[j].note == note:
                                skip.append(j)
                               # length -= self.track[j].time
                                break
                        j += 1
                    length *= self.seconds
                    fopen.write("{}\t\t".format(n))
                    fopen.write("{:4.5f}\t\t".format(t))
                    fopen.write("{}\t\t".format(note2char(msg.note)))
                    fopen.write("{:3}\t\t".format(msg.velocity))
                    fopen.write("{:3.5f}\t\t".format(length))
                    fopen.write("{}\n".format(msg.time))
                    n += 1
    def readTrackFile(self, filename, fro = 0, to = -1):
        ## Clear track
        self.clear()
        from utils import splitLine, note2char
        fopen = open(filename)
        line = fopen.readline().strip()
        i = -1
        total = 0
        currTime = 0
        timeShift = 0
        coming = {}
        ## Read file
        while line != "":
            ## Remove comments
            line = line.split('%')[0]
            if line != "":
                i += 1
                if i == 0:
                    # First line
                    self.ticksPerBeat = int(line)
                elif i == 1:
                    # Second line
                    self.beatsPerMinute = int(line)
                elif i == 2:
                    # Third line
                    total = int(line)
                    if to == -1:
                        to = total / 2
                else:
                    # Parse line's info
                    try:
                        _id, time, note, velocity, length = splitLine(line)
                        time += timeShift
                    except ValueError:
                        ## Line can't be parsed
                        # So it's probably a time-shift
                        if line.startswith('t'):
                            line = line.replace(' ','')
                            shift = float(line[1:])
                            timeShift += shift
                        elif line.startswith("pedal"):
                            if line.endswith("on"):
                                # Add pedal on (ctrl_ch,ctrl=64,val=127)
                                print("Added {}".format(PEDAL_ON))
                                self.appendMsg(PEDAL_ON)
                            elif line.endswith("off"):
                                print("Added {}".format(PEDAL_OFF))
                                self.appendMsg(PEDAL_OFF)
                        # Skip to next line
                        _id = -1
                    # If it's within range
                    if _id >= fro and _id <= to:
                        while time in coming:
                            # No repeated, overwritten msgs
                            time += 0.00000001
                        # Add message to qeue
                        coming[time] = [note, velocity]
                        while time+length in coming:
                            # No repeated, overwritten msgs
                            length += 0.00000001
                        # And add the closing one (lift finger off key)
                        coming[time+length] = [note, 0]
                        ## All done, add all necessary messages (until we reach current time)
                        times = coming.keys()
                        times.sort(reverse=True) # Sort first is last
                        while currTime != time:
                            t = times.pop()
                            note, velocity = coming.pop(t)
                            delay = abs(t - currTime)
                            self.appendNote(note, velocity, delay, True)
                            currTime = t
            line = fopen.readline().strip()
        i = 0
        while 1:
            self.track[i].time = 0
            if self.track[i].type == "note_on":
                break
            i += 1

    def loadFile(self, filename):
        self.track = [] # Clear track
        midi = MidiFile(filename)
        track = midi.tracks[0]
        self.ticksPerBeat = midi.ticks_per_beat
        try:
            while 1:
                msg = track.pop()
                if msg.type in to_be_taken:
                    self.track.append(msg)
        except IndexError:
            self.track.reverse()
    def saveFile(self, filename):
        midi = MidiFile()
        midi.tracks.append(self.track)
        midi.ticks_per_beat = self.ticksPerBeat
        midi.save(filename)
    ## getLength
    def getLength(self):
        return [self.getLengthInSec(),self.getLengthInBeats(),self.getLengthInTicks()]
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
        length = 1.*length / self.ticksPerBeat
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
        msg.time = time if seconds == False else int(round(time / self.seconds))
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
        ticks = beats * self.ticksPerBeat
        length = self.getLengthInTicks()
        if length == 0:
            return None
        n = float(ticks)
        if length > ticks:
            while abs(length - n) > (ticks / 2):
                n += ticks
        k = n / length
        self.scale(k)
    def scale(self, scaleFactor):
        for msg in self.track:
            msg.time = int(round(msg.time * scaleFactor))
