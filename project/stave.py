from track import Track
from sys import argv

fname = argv[1]

track = Track()
track.loadFile(fname)
length = track.getLength()

notes = {}

# copy list and reverse, so we can pop the messages out and leave track intact
msgs = list(track.track).reverse() 

ticks = 0
msg = msgs.pop()
while ticks * 60.0 / track.ticksPerBeat / track.beatsPerMinute < length:
    while msg.type != "note_on":
        msg = msgs.pop()

        try:
            if notes[msg.value
        if msg.value not in notes:
            notes[msg.value] = True
        ticks += 1
        msg.time -= 1
        if msg.time == 0: # Time to get the next msg
            msg = msgs.pop()
    else: ## It's a control msg, so get a new one
        msg = msgs.pop()
