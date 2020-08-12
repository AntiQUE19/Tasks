from tkinter import *
from R2Graph import *
from math import *
from time import *

sizeX = 300
sizeY = 300
rx = (sizeX - 20)/2
ry = (sizeY - 20)/2
cx = sizeX/2
cy = sizeY/2
center = R2Point(cx, cy)

rootWindow = Tk()
rootWindow.title("Clock")
# rootWindow.geometry("300x300")
rootWindow.geometry(str(sizeX) + "x" + str(sizeY))
idHourArrow = 0
idMinArrow = 0
idSecArrow = 0

drawArea = Canvas(
    rootWindow,
    width=sizeX, height=sizeY,
    bg="lightGray"
)
drawArea.place(anchor="nw", x=0, y=0)

# Draw face
drawArea.create_oval(
    (cx - rx, cy - ry), 
    (cx + rx, cy + ry),
    fill = "silver", outline="blue", width=4
)

def alpha(minutes):
    return (minutes*6)*pi/180.

for m in range(60):
    a = alpha(m)
    v = R2Vector(rx*sin(a), -ry*cos(a))
    p0 = center + v*0.95
    if (m % 5 == 0):
        if (m % 15 != 0):
            p0 = center + v*0.9
        else:
            p0 = center + v*0.8
    p1 = center + v
    drawArea.create_line(
        (p0.x, p0.y), (p1.x, p1.y), 
        fill="blue", width=2
    )
    
def drawTime():
    global idHourArrow
    global idMinArrow
    global idSecArrow
    
    t = localtime(time())
    hour = t.tm_hour
    minutes = t.tm_min
    seconds = t.tm_sec
    # print(str(hour)+":"+str(minutes)+":"+str(seconds))
    
    a = alpha((hour + minutes/60.)*5)
    v = R2Vector(rx*sin(a), -ry*cos(a))
    t0 = center - v*0.1
    t1 = center + v*0.5
    if (idHourArrow != 0):
        drawArea.delete(idHourArrow)
    idHourArrow = drawArea.create_line(
        (t0.x, t0.y), (t1.x, t1.y), 
        fill="black", width=7
    )

    a = alpha(minutes + seconds/60.)
    v = R2Vector(rx*sin(a), -ry*cos(a))
    t0 = center - v*0.2
    t1 = center + v*0.7
    if (idMinArrow != 0):
        drawArea.delete(idMinArrow)
    idMinArrow = drawArea.create_line(
        (t0.x, t0.y), (t1.x, t1.y), 
        fill="darkGreen", width=5
    )

    a = alpha(seconds)
    v = R2Vector(rx*sin(a), -ry*cos(a))
    t0 = center - v*0.25
    t1 = center + v*0.8
    if (idSecArrow != 0):
        drawArea.delete(idSecArrow)
    idSecArrow = drawArea.create_line(
        (t0.x, t0.y), (t1.x, t1.y), 
        fill="red", width=3
    )
    
    drawArea.after(1000, drawTime)
    
drawTime()
rootWindow.mainloop()
