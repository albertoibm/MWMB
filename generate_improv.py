from piano.piano import Piano
from piano.player import Player
from piano.track import Track

from random import random
from time import sleep

from sys import argv

letters = ["C","C#","D","Eb","E","F","F#","G","G#","A","Bb","B"]
scale = [0,2,4,5,7,9,11]
major = [0,4,7]
minor = [0,3,7]

use = major
notes = 2
usekey = False
force = 0.80

def usage():
    print "Usage: %s <options>"%argv[0]
    print ""
    print "Options:"
    print "-h \tThis help"
    print "-M \tUse major chord"
    print "-m \tUse minor chord"
    print "-s \tUse whole scale"
    print "-n N\tMaximum number of notes to play after a key is pressed"
    print "-k \tUse the key pressed or the scale key as a base to improvise"
    print "-f F\tForce with wich to play notes after key is pressed in percentage"
def improvise(msg):
    track = Track()
    length = 1 + 2 * int(round((notes-1) * random()))
#    base = msg.note
    for i in range(length):
        octave = int(round(random() * 4 - 1))
        #octave = int(msg.note / 12) # same octave
        if usekey:
            note = msg.note + octave * 12 +\
                    use[int(random() * len(use))]
        else:
            note = base + octave * 12 +\
                    use[int(random() * len(use))]
        length = 0.125 * int(1 + 7 * random())
        velocity = int(round(msg.velocity * force))
        track.appendNote(note, velocity, 0)
        track.appendNote(note, 0, length, seconds = True)
    return track
def play(msg):
    if msg.type == "note_on" and msg.velocity != 0:
        track = improvise(msg)
        player = Player()
        player.setPiano(piano)
        player.start()
        player.setTrack(track)
        player.playOnce()

if "-h" in argv:
    usage()
    exit()
if "-M" in argv:
    use = major
if "-m" in argv:
    use = minor
if "-s" in argv:
    use = scale
if "-n" in argv:
    notes = int(argv[argv.index("-n")+1])
if "-k" in argv:
    usekey = True
if "-f" in argv:
    force = 1.0 / 100 * int(argv[argv.index("-f")+1])

piano = Piano()
piano.autoconnect()
print("Press the key on which the scale is based")
msg = piano.receive()
base = msg.note
print (base/12)
Note = letters[base%12]+str(base/12)
print("Using scale on "+Note)
#wait for key release
piano.receive()
piano.setCallback(play)
try:
    while 1:
        sleep(0.1)
except KeyboardInterrupt:
    print("Ciao bello(a)!")
