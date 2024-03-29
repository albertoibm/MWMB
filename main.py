from sys import argv
from random import random
from time import sleep

from piano.piano import Piano
from piano.track import Track
from piano.player import Player
from piano.recorder import Recorder
from piano.logger import Logger
from piano.button import Button,Status
from piano.ui import UI
import piano.codec as codec

class MWMB:
    def __init__(self, piano = None, in_ = None, out_ = None, quiet = True):
        self.piano = piano
        self._in = in_
        self._out = out_
        self.rec = Recorder()
        self.pad = {}
        self.logger = None
        self.setup(quiet)
    def setup(self, quiet):
        if self.piano == None:
            self.piano = Piano()
        [ins,outs] = self.piano.listDevices()
        if self._in == None:
            self._in = ins[0]
        if self._out == None:
            self._out = outs[0]
        if self.logger == None:
            self.logger = Logger(self.piano, self.rec, quiet)
    def connect(self):
        if self._in != None and self._out != None:
            self.piano.connect(self._in, self._out)
            self.rec.setPiano(self.piano)
    def reconnect(self):
        self._in = None
        self._out = None
        self.setup()
        self.connect()
    def run(self):
        keys = ['7','8','9',\
                '4','5','6',\
                '1','2','3']
 #       self.piano.connect(self._in, self._out)
#        self.rec.setPiano(self.piano)
        self.connect()

        ui = UI()
        ui.startColor()
        height,width = list(map(int,ui.size()))
        h3 = int(round(height/3))
        w3 = int(round(width/3))
        # Create buttons
        for key in keys:
            idx = keys.index(key)
            x = int(idx % 3) * w3
            y = int(idx / 3) * h3
            win = ui.newWindow(h3,w3,"btn_{}".format(key),x,y)
            self.pad[key] = Button(self.piano, self.rec, win, int(key))
        ui.refresh()
        for k in keys:
            ui.setWindow(self.pad[k].window())
            ui.setColorPair(262)
            ui.fill()
            ui.refresh()

        # Run loop
        selected = None
        while 1:
            _k = ui.getChar()
            k = chr(_k) if _k < 256 else _k
            if k != _k:
                ui.log(k)
#            k = raw_input(">")
            if k in keys:
                status = self.pad[k].press()
                ui.setWindow(self.pad[k].window())
                if status == Status.Playing:
                    color = 286
                elif status == Status.Recording:
                    color = 266
                elif status == Status.Ready:
                    color = 281
                else:
                    color = 262
#                color = 259+int(random()*40)
                ui.setColorPair(color)
                ui.fill()
                length = self.pad[k].getLength()
                toprint = str(status)+"\n"
                toprint += "length:\n"
                toprint += "{} s\n".format(length[0])
                toprint += "{} beats\n".format(length[1])
                toprint += "{} ticks".format(length[2])
                ui.putStrWin(toprint)
                ui.log("{}".format(status.name))
            elif k == "c":
                ui.log("Clear. Select a Track")
                _t = ui.getChar()
                t = chr(_t) if _t < 256 else _t
                if t in keys:
                    self.pad[t].doublePress()
                    color = 262
                    ui.setWindow(self.pad[t].window())
                    ui.setColorPair(color)
                    ui.fill()
                    ui.log("Cleared")
                else:
                    ui.log("Aborted")
            elif k == "r":
                ui.log("Reconnecting")
                self.piano.autoconnect()
            elif k == "s":
                ui.log("Saving session")
                codec.write(self.pad)
            elif k == "p":
                ui.log("Reset piano (Panic)")
                self.piano.output.panic()
            # Exit if k == ESC or 'q'
            elif _k == 27 or k == "q":
                ui.log("Exiting")
                ui.refresh()
                break
            ui.refresh()
            self.logger.writeBuffer()

        # Exit
        self.logger.close()
        ui.log("Stopping players")
        for key in self.pad:
            self.pad[key].stop()
        ui.quit()

def usage():
    print("Usage:")
    print("")
    print(("%s <options>"%argv[0]))
    print("")
    print("-h or --help\tThis help")
    print("-i or --input\tChoose an input Midi device from a list of available ones")
    print("-o or --output\tChoose an output Midi device from a list of available ones")
    print("-q or --quiet\tDo not log the session")
    print("-l or --log\tLog the session")

if __name__ == "__main__":
    if "-h" in argv or "--help" in argv:
        usage()
        exit()
    # Log only if -l (log) in arg and -q (quiet) not in arg. quiet by default then
    quiet = ("-l" not in argv and "--log" not in argv) or ("-q" in argv or "--quiet" in argv)
    piano = Piano()
    [ins,outs] = piano.listDevices()
    if "-i" in argv or "--input" in argv:
        print("[+] List of input devices")
        for i in range(len(ins)):
            print("%d: %s"%(i+1,ins[i]))
        inDev = ins[int(input("Select input device: "))-1]
    else:
        inDev = ins[0]
    if "-o" in argv or "--output" in argv:
        print("[+] List of output devices")
        for i in range(len(outs)):
            print("%d: %s"%(i+1,outs[i]))
        outDev = outs[int(input("Select output device: "))-1]
    else:
        outDev = outs[0]

    main = MWMB(piano, inDev, outDev)
    main.run()
