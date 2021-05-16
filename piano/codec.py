from time import ctime
def read(fileName):
    try:
        fopen = open(fileName)
    except IOError as e:
        print(e)
        exit()
    pad = {}
def write(pad):
    sessionName = ctime().replace(" ","_")
    fileName = "./{}.pad".format(sessionName)
    fopen = open(fileName,'w')
    for key in pad:
        fopen.write(key+":")
        track = pad[key].player.track
        if track != None:
            for msg in track.track:
                fopen.write(str(msg.note)+",")
                fopen.write(str(msg.velocity)+",")
                fopen.write(str(msg.time)+";")
        fopen.write("\n")
    fopen.close()
