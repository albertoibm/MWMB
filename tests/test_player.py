from piano import Piano
from recorder import Recorder
from player import Player
from sys import argv
import mido

### Call python test_recorder.py
##
## Options:
##      -i      Select input device
##      -o      Select output device

### Options
verbose = "-v" in argv

### Create instance of Piano, Recorder and Player
p = Piano()
rec = Recorder()
player = Player()
player.start() # Start thread

### Connecting player with piano
player.setPiano(p)

### Select input and output devices
[ins,outs] = p.listDevices()
if "-i" in argv:
    print("[+] List of input devices")
    for i in range(len(ins)):
        print("%d: %s"%(i+1,ins[i]))
    inDev = ins[int(input("Select input device: "))-1]
else:
    inDev = mido.get_input_names()[0]

if "-o" in argv:
    print("[+] List of output devices")
    for i in range(len(outs)):
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

### Receive track from recorder
player.setTrack(rec.emit())

### Play it back in a loop
input("Testing playback. Press enter")
player.play()
print("List of commands:")
print("p\t\tPlay/Pause")
print("+\t\tTranspose one tone up")
print("-\t\tTranspose one tone down")
print(">\t\tSpeed up playback")
print("<\t\tSpeed down playback")
print("q\t\tQuantize")
print("x\t\tExit")
usrInput = input("> ")
while usrInput != "x":
    if usrInput == "+":
        player.transpose("+1")
    elif usrInput == "-":
        player.transpose("-1")
    elif usrInput == "p":
        player.toggle()
    elif usrInput == ">":
        player.speedUp(10)
    elif usrInput == "<":
        player.speedDown(10)
    elif usrInput == "q":
        print("Quantize to:")
        print("1) 8")
        print("2) 16")
        print("3) 32")
        print("4) 64")
        print("5) 128")
        usrInput = input("> ")
        if usrInput == "1":
            player.quantize(8)
        elif usrInput == "2":
            player.quantize(16)
        elif usrInput == "3":
            player.quantize(32)
        elif usrInput == "4":
            player.quantize(64)
        elif usrInput == "5":
            player.quantize(128)
    try:
        usrInput = input("> ")
    except:
        break

#raw_input("Stop playback. Press enter")
player.play(False)
player.stop() # Stops thread
player.join()
