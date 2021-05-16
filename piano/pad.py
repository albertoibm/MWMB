Purple = 262
Green = 286
Red = 266
Blue = 281
class Pad:
    def __init__(self,piano=None,rec=None,ui=None):
        self.piano = piano
        self.rec = rec
        self.ui = ui
        self.keys = {}
    def setPiano(self,piano):
        self.piano = piano
    def setRecorder(self,rec):
        self.rec = rec
    def setUI(self,ui):
        self.ui = ui
    def addKey(self,key,shape):
        width,height,x,y = shape
        win = self.ui.newWindow(height,width,"btn_{}".format(key),x,y)
        self.keys[key] = Button(self.piano, self.rec, win)
        self.colorKey(key,Purple)
    def colorKey(self,key,color):
        window = self.keys[key].window()
        self.ui.setWindow(window)
        ui.setColorPair(color)
        ui.fill()
    def refresh(self):
        ui.refresh()
