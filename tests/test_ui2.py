from ui import UI
from time import sleep
import curses

ui = UI()
ui.startColor()
height,width = list(map(int,ui.size()))

buttons = []
for i in range(9):
    ui.log("Creando ventana btn{}".format(i))
    sleep(0.3)
    x = int(round((i%3) * (width/3)))
    y = int(round((i/3) * (height/3)))
    buttons.append( ui.newWindow(int(round(height/3)),int(round(width/3)),"btn{}".format(i),x,y) )
    ui.log("Listo! Seleccionando ventana y color...")
    sleep(0.3)
    ui.setWindow(buttons[i])
    ui.setColorPair(i*9)
    ui.log("Listo! Rellenando ventana")
    ui.fill("/")
    ui.refresh()
while 1:
    k = ui.getChar()
    ui.log("Pressed key {}".format(k))
    if k == 27: 
        ui.log("Exiting...")
        ui.refresh()
        break
    ui.refresh()
ui.quit()
