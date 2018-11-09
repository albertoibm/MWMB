from piano import Piano
from recorder import Recorder
from player import Player
from track import Track
from sys import argv
import mido

### Call python test_track.py
##
## Options:
##      -i          Select input device
##      -o          Select output device
##      -f FILE     Select file to load
##      -v          Verbose
##      -q NUM      Quantize to NUM (8,16,32,64)

### Options
verbose = "-v" in argv

### Testing loadFile
try:
    filename = argv[argv.index("-f")+1]
except ValueError:
    print "Error. You have to specify a filename!"
    print ""
    print "Usage:"
    print "python test_track.py -f filename"
    exit()
except IndexError:
    print "Missing arguments"
    exit()

### Quantization
if "-q" in argv:
    quant = int(argv[argv.index("-q")+1])
else:
    quant = 16

### Create instance of Piano, Recorder, Player and Track
p = Piano()
rec = Recorder()
track = Track()
player = Player()
player.start() # Start thread

### Connecting player with piano
player.setPiano(p)

### Select input and output devices
[ins,outs] = p.listDevices()
if "-i" in argv:
    print "[+] List of input devices"
    for i in range(len(ins)):
        print "%d: %s"%(i+1,ins[i])
    inDev = ins[int(raw_input("Select input device: "))-1]
else:
    inDev = mido.get_input_names()[0]

if "-o" in argv:
    print "[+] List of output devices"
    for i in range(len(outs)):
        print "%d: %s"%(i+1,outs[i])
    outDev = ins[int(raw_input("Select output device: "))-1]
else:
    outDev = mido.get_output_names()[0]

### Connecting to input and output devices
print "Testing inDev and outDev"
if p.connect(inDev,outDev) :
    if verbose:
        print "PASSED"
else:
    if verbose:
        print "FAILED"

track.loadFile(filename)
track.scaleToBar()
print "Testing quantize %d"%quant
track.quantize(quant)
player.setTrack(track)
player.play()
raw_input("Press Enter to exit")
player.play(False)
player.stop()
player.join()
