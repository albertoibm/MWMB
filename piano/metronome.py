import threading
from time import sleep
class Metronome(threading.Thread):
    def __init__(self, f_ = None, dt = 0.5):
        self._f = f_
        self.dt = dt
        self.running = True
    def play(self):
        self.playing = True
    def pause(self):
        self.playing = False
    def run(self):
        while self.running:
            while self.playing:
                sleep(self.dt)
                print ("Calling _f()")
                self._f()
    def stop(self):
        self.running = False

