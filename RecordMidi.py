from piano.piano import Piano
from piano.recorder import Recorder
from sys import argv
import mido

### Call python test_recorder.py
##
## Options:
##      -i      Select input device
##      -o      Select output device

### Create instance of Piano and Recorder
p = Piano()
rec = Recorder()

### Options
verbose = "-v" in argv

### Select input and output devices
if "-i" in argv:
    [ins,outs] = p.listDevices()
    print "[+] List of input devices"
    for i in range(len(ins)):
        print "%d: %s"%(i+1,ins[i])
    inDev = ins[int(raw_input("Select input device: "))-1]
else:
    inDev = mido.get_input_names()[0]

if "-o" in argv:
    print "[+] List of output devices"
    for i in range(len(ins)):
        print "%d: %s"%(i+1,outs[i])
    outDev = ins[int(raw_input("Select output device: "))-1]
else:
    outDev = mido.get_output_names()[0]

### Connecting to input and output devices
if not p.connect(inDev,outDev) :
    if verbose:
        print "FAILED"
    exit()

### Connecting recorder with piano
if not rec.setPiano(p):
    if verbose:
        print "setPiano() returned error!"
    exit()


### Record something
print "Recording from "+inDev
rec.record()    
track = rec.emit()
name = raw_input("Filename: ")
name = name.replace(" ","_")
name = name.replace("/","-")
track.saveFile(name+".mid")
