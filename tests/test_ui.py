from ui import UI
from time import sleep
import curses

ui = UI()
ui.startColor()
height,width = list(map(int,ui.size()))

ui.setColorPair(0)
ui.putStrXY(10, 1, "Height = {}".format(height))
ui.putStrXY(10, 2, "Width = {}".format(width))
ui.putStrXY(10, 3, "Continue to newWindow()")
k = ui.getChar()

newwin = ui.newWindow(int(round(height/2)),int(round(width/2)),"main",int(round(width/2)),int(round(height/2)))
ret = ui.setWindow(newwin)
for x in range(int(round(width/2))-1):
    for y in range(int(round(height/2))-1):
        pair = y * height + x
        ui.setColorPair(pair)
        ui.putStr("x")
ui.refresh()
ui.setColorPair(0)
ui.putStr("ret = {}".format(ret))
ui.setCursor(0,0)
ui.putStr("Press any key to continue")
ui.setWindow("")
while 1:
    k = ui.getChar()
    ui.log("Pressed key {}".format(k))
    if k == 27: 
        ui.log("Exiting...")
        ui.refresh()
        break
    elif k == 10: # Enter
        ui.setWindow("main")
        ui.clear()
    elif k == 99: # c
        ui.setWindow("")
    elif k == 109: # m
        ui.setWindow("main")
    elif k == 102: # f
        ui.fill(".")
    else:
        ui.setColorPair(k)
        ui.putStrXY(0,0,"Pressed KEY ({}). WRONG. Try another one".format(k))
    ui.refresh()
ui.quit()
