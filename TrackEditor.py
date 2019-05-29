from sys import argv
from time import sleep

from piano.track import Track
from piano.player import Player
from piano.piano import Piano

LO = unichr(9603)
HI = unichr(9600)
MD = unichr(9644)

if len(argv) < 2:
    print "Usage:"
    print argv[0] +  " [.trk file] <options>"
    print "-f <0>\t\tFrom line number"
    print "-t <0>\t\tTo line number"
    print "-a <0>\t\tAround line number (20 lines)"
    print "-s    \t\tSave .trk file"
    print "-m    \t\tSave .mid file"
    exit()

if "-f" in argv:
    fro = int(argv[argv.index("-f")+1])
else:
    fro = 0

if "-t" in argv:
    to = int(argv[argv.index("-t")+1])
else:
    to = -1
if "-a" in argv:
    around = int(argv[argv.index("-a")+1])
    fro = max(0, around - 20)
    to = around + 20
else:
    around = 0
save = "-s" in argv
midi = "-m" in argv

fname = argv[1]

track = Track()
#try:
track.readTrackFile(fname, fro, to)
#except:
#    exit("Wrong filename {}".format(fname))

p = Piano()
player = Player()
player.start()
player.setPiano(p)
p.autoconnect()

player.setTrack(track)

player.setN(fro)
player.playOnce(verbose=True)
try:
    sleep(track.getLengthInSec())
except:
    if raw_input("Quit? (y/n)") == 'y':
        player.pause()
player.stop()

if save:
    track.writeTrackFile(fname+".corr")
if midi:
    track.saveFile(fname+".mid")
