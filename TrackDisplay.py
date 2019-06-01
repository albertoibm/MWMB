from sys import argv

from piano.track import Track
from piano.player import Player
from piano.piano import Piano

from piano.ui import UI
from piano.display import Display


if len(argv) < 2:
    print "Usage:"
    print argv[0] + " [.trk file]"
    exit()

## Read trk file
fname = argv[1]
track = Track()
track.readTrackFile(fname)

ui = UI()
ui.startColor()
widht,height = map(int, ui.size())

win = ui.newWindow

display = Display(ui, track)
display.createList()

while 1:
    _k = ui.getChar()
    ui.clear()
#    ui.setColorPair(260)
    k = chr(_k) if _k < 256 else _k
    if _k == 259: # up
        display.up()
    elif _k == 339: # pg up
        display.pgup()
    elif _k == 258: # down
        display.down()
    elif _k == 338: # pg down
        display.pgdown()
    elif _k == 260: # left
        display.left()
    elif _k == 261: # right
        display.right()
    elif _k == 10: # enter
        display.enter()
    elif _k == 27 or k == "q":
        break
    else:
        ui.setColorPair(200)
        print "%d"%_k
    display.update()
    ui.log("%d"%_k)
    ui.refresh()
ui.quit()
print "%d"%_k
