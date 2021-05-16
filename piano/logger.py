from time import ctime
class Logger:
    def __init__(self,piano = None, rec = None, quiet = False):
#        print("Logger created")
        self.quiet = quiet
        self.setRecorder(rec)
        self.setPiano(piano)
        self.sessionName = ctime().replace(" ","_")
        self.fileName = "./{}.imf".format(self.sessionName)
        self.fileOpen = None
        self.buffer = []
        self.writeHeader()
    def write(self,entry):
        if not self.quiet:
            self.openFile()
            if type(entry) is str:
                self.fileOpen.write(entry)
            elif type(entry) is list or type(entry) is tuple:
                for item in entry:
                    self.fileOpen.write(item)
            self.closeFile()
    def writeHeader(self):
        self.write("## Improvisation Machine Format\n")
        self.write("# Session: {}\n".format(self.sessionName))
    def writeBuffer(self):
        self.write(self.buffer)
    def close(self):
        if len(self.buffer) > 0:
            self.writeBuffer()
    def openFile(self):
        self.fileOpen = open(self.fileName,'a')
    def closeFile(self):
        self.fileOpen.close()
    def log(self,msg):
        self.buffer.append(self.readMsg(msg))
#        print("Logged msg "+self.buffer[-1])
    def readMsg(self,msg):
        if msg.type == "note_on":
            return "n{},t{},v{};".format(msg.note,msg.time,msg.velocity)
        return ""
    def setPiano(self,piano):
        self.piano = piano
        if self.piano != None:
            self.piano.setLogger(self)
    def setRecorder(self,rec):
        self.rec = rec
        if self.rec != None:
            self.rec.setLogger(self)
