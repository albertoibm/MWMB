###
import mido
class Piano:
    def __init__(self):
        self.output = None
        self.input = None
        self.logger = None
    def send(self,note=0, velocity = 0):
        if self.output == None:
            return 0
        else:
            msg = mido.Message("note_on")
            msg.note = note
            msg.velocity = velocity
            self.output.send(msg)
            return 1
    def sendMsg(self,msg):
        if self.output == None:
            return 0
        else:
            self.output.send(msg)
            self.logMsg(msg)
            return 1
    def setCallback(self,f):
        if self.input != None:
            if not self.input.closed:
                self.input.callback = f
                return 1
            else:
                print("Connection with input device already closed!")
                return 0
        else:
            print("No input device!")
            return 0
    def setLogger(self,logger):
        self.logger = logger
    def logMsg(self,msg):
        if self.logger != None:
            self.logger.log(msg)
    def receive(self):
        if self.input == None:
            return 0
        else:
            return self.input.receive()
    def autoconnect(self):
        [ins,outs] = self.listDevices()
        if ins[0] != None and outs[0] != None:
            self.connect(ins[0],outs[0])
    def connect(self,in_ch,out_ch=""):
        if out_ch == "": out_ch = in_ch
        try:
            print("Connected to %s"%out_ch)
            self.output = mido.open_output(out_ch)
        except IOError:
            print("Unknown output port",out_ch)
            return 0
        try:
            print("Connected to %s"%in_ch)
            self.input = mido.open_input(in_ch)
        except IOError:
            print("Unknown input port",in_ch)
            return 0
        return 1 # All well
    def listDevices(self):
        ins = mido.get_input_names()
        outs = mido.get_output_names()
        return [ins,outs]


