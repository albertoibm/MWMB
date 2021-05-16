from piano import Piano
from recorder import Recorder
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
    print("[+] List of input devices")
    for i in range(len(ins)):
        print("%d: %s"%(i+1,ins[i]))
    inDev = ins[int(input("Select input device: "))-1]
else:
    inDev = mido.get_input_names()[0]

if "-o" in argv:
    print("[+] List of output devices")
    for i in range(len(ins)):
        print("%d: %s"%(i+1,outs[i]))
    outDev = ins[int(input("Select output device: "))-1]
else:
    outDev = mido.get_output_names()[0]

### Connecting to input and output devices
print("Testing inDev and outDev")
if p.connect(inDev,outDev) :
    if verbose:
        print("PASSED")
else:
    if verbose:
        print("FAILED")

### Connecting recorder with piano
print("Testing recorder and piano connection")
if rec.setPiano(p):
    if rec.piano == p and rec.handler == p.input.callback:
        if verbose:
            print("PASSED")
    else:
        if verbose:
            print("FAILED")
else: 
    if verbose:
        print("setPiano() returned error!")
        print("FAILED")


### Record something
print("Testing recording")
rec.record()    

### Play it back in a loop
input("Testing playback. Press enter")
while 1:rec.play()
