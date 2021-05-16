from piano import Piano
from time import sleep
p = Piano()
[ins,outs] = p.listDevices()
print("[+] List of input devices")
for i in range(len(ins)):
    print("%d: %s"%(i+1,ins[i]))
inDev = ins[int(input("Select input device: "))-1]

print("[+] List of output devices")
for i in range(len(ins)):
    print("%d: %s"%(i+1,outs[i]))
outDev = ins[int(input("Select output device: "))-1]

print("Testing Send()")
if p.connect(inDev,outDev):
    p.send(50,80)
print("Testing Receive(). Press a key on the piano")
print(p.receive())
called = lambda x:exit()
p.setCallback(called)
print("Testing callback. Press a key on the piano")
while 1:
    sleep(0.1)
    pass
