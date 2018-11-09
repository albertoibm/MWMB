from sys import argv

import mido
from piano import Piano
from recorder import Recorder
from player import Player
from button import Button

## Setup Piano
piano = Piano()
[ins,outs] = piano.listDevices()
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
piano.connect(inDev,outDev)

## Setup Recorder
rec = Recorder()
if not rec.setPiano(piano):
    exit("Could not connect to piano!")

## Setup players/buttons
nButtons = 9
buttons = {}
for i in range(nButtons):
    buttons[i] = Button(piano,rec)

## Run test
print "0-9 to press button"
print "q to quit"
userInput = None
button = None
while userInput != "q":
    userInput = raw_input("> ")
    try:
        button = int(userInput)
        if button in buttons.viewkeys():
            buttons[button].press()
    except ValueError:
        if userInput == "q":
            for key in buttons:
                buttons[key].stop()
        elif userInput.startswith("d"):
            try:
                button = int(userInput[1:])
                buttons[button].doublePress()
            except:
                pass
