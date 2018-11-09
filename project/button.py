from player import Player
from enum import Enum
class Status(Enum):
    """
    Status = 0b00
               ||
 Playing/Rec<--  -->Clear/Ready
    """
    Clear = 0
    Ready = 1
    Playing = 2
    Recording = 4
class Button:
    """
    button = Button(piano,recorder)
    button.press()          # Record
    button.press()          # Stop recording
    button.press()          # Start playback
    button.press()          # Pause playback
    button.doublePress()    # Set to record again
    """
    def __init__(self,piano=None,rec=None):
        self.status = Status.Clear
        self.player = Player()
        self.player.start()
        self.setPiano(piano)
        self.setRecorder(rec)
    def stop(self):
        self.player.stop()
    def setPiano(self,piano):
        self.piano = piano
        self.player.setPiano(self.piano)
    def setRecorder(self,rec):
        self.rec = rec
    def press(self):
        if self.status == Status.Clear:
            # Clear to Rec
            print "Status: Clear -> Rec"
            if not self.rec.recording:
                self.rec.clear()
                if self.rec.startRecording():
                    self.status = Status.Recording
        elif self.status == Status.Ready:
            ## Ready to Playing
            print "Status: Ready <-> Playing"
            self.player.toggle()
            #self.status == Status.Playing
        elif self.status == Status.Recording:
            ## Rec to Ready
            print "Status: Rec -> Ready"
            if self.rec.recording:
                self.rec.stopRecording()
                track = self.rec.emit()
                track.scaleToBar(2)
                self.player.setTrack(track)
                self.rec.clear()
                self.status = Status.Ready
        elif self.status == Status.Playing:
            ## Playing to Ready
            print "Status: Playing -> Ready"
            self.player.pause()
            self.status == Status.Ready
    def doublePress(self):
        self.status = Status.Clear
