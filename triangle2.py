from tkinter import *
from R2Graph import *

def main():
    rootWindow = Tk()
    rootWindow.title("Triangle")
    rootWindow.geometry("800x600")

    points = []
    catchPointIdx = (-1)
    dragPointIdx = (-1)
    drawTriangle = False

    def findPoint(p):
        nonlocal points
        for i in range(len(points)):
            if p.distance(points[i]) < 4:
                return i
        return (-1)

    panel = Frame(rootWindow)
    drawArea = Canvas(rootWindow, bg="lightBlue")

    def clear():
        nonlocal catchPointIdx, dragPointIdx, drawTriangle
        drawArea.delete("all")
        points.clear()
        catchPointIdx = (-1) 
        dragPointIdx = (-1)
        drawTriangle = False
        drawArea.configure(cursor="")

    clearButton = Button(panel, text="Clear", command=clear)

    def redraw():
        drawArea.delete("all")
        for p in points:
            # draw a cross in the point
            drawArea.create_line(
                p.x - 8, p.y, p.x + 8, p.y, fill="red", width=3
            )
            drawArea.create_line(
                p.x, p.y-8, p.x, p.y+8, fill="red", width=3
            )
        if len(points) >= 3 and drawTriangle:
            # draw triangle and inscribed circle
            drawArea.create_line(
                points[0].x, points[0].y,
                points[1].x, points[1].y,
                points[2].x, points[2].y,
                points[0].x, points[0].y,
                fill="blue", width=2
            )
            (center, radius, bisectrixes) = inCircle(points)
            # Draw an inscribed circle
            drawArea.create_oval(
                center.x - radius, center.y - radius,
                center.x + radius, center.y + radius,
                fill="", outline="red", width=2
            )
            # Draw bisectrixes
            for i in range(3):
                drawArea.create_line(
                    points[i].x, points[i].y,
                    bisectrixes[i].x, bisectrixes[i].y,
                    fill="darkGreen", width=1
                )
            # Draw the center of circle
            drawArea.create_oval(
                center.x - 4, center.y - 4,
                center.x + 4, center.y + 4,
                fill="red", outline="red"
            )

    def onDraw():
        nonlocal drawTriangle
        if len(points) >= 3:
            drawTriangle = True
            redraw()

    drawButton = Button(panel, text="Draw", command=onDraw)

    panel.pack(fill=X, padx=4, pady=4)
    clearButton.pack(side=LEFT)
    drawButton.pack(side=LEFT)
    drawArea.pack(fill=BOTH, side=TOP, expand=True, padx=4, pady=4)

    def onMouseRelease(e):
        nonlocal catchPointIdx, dragPointIdx
        if dragPointIdx < 0:
            if len(points) >= 3:
                clear()
            points.append(R2Point(e.x, e.y))
        else:
            points[dragPointIdx] = R2Point(e.x, e.y)
        catchPointIdx = (-1); dragPointIdx = (-1)
        drawArea.configure(cursor="")
        redraw()

    drawArea.bind("<ButtonRelease-1>", onMouseRelease)

    def onMotion(e):
        nonlocal catchPointIdx, dragPointIdx

        if dragPointIdx >= 0:
            # move the dragging point to the new position
            points[dragPointIdx] = R2Point(e.x, e.y)
            redraw()
        else:
            idx = findPoint(R2Point(e.x, e.y))
            if idx >= 0 and catchPointIdx < 0:
                drawArea.configure(cursor="hand1")
            elif idx < 0 and catchPointIdx >= 0:
                drawArea.configure(cursor="")
            catchPointIdx = idx

    drawArea.bind("<Motion>", onMotion)

    def onMousePress(e):
        nonlocal catchPointIdx, dragPointIdx
        if catchPointIdx >= 0:
            dragPointIdx = catchPointIdx
            catchPointIdx = (-1)
            drawArea.configure(cursor="dot") # sailboat center_ptr hand2

    drawArea.bind("<Button-1>", onMousePress)

    rootWindow.mainloop()

# Compute bisectrixes of triangle and 
# a center & radius of inscribed circle
def inCircle(vertices):
    bisectrixes = []
    for i in range(3):
        iPrev = i - 1
        if iPrev < 0:
            iPrep = 2
        iNext = i + 1
        if iNext >= 3:
            iNext = 0
        vPrev = (vertices[iPrev] - vertices[i]).normalized()
        vNext = (vertices[iNext] - vertices[i]).normalized()
        b = vPrev + vNext   # The direction vector of i-th bisectrix

        # The point of bisectrix is calculated as intersection of 2 lines,
        # where a line is defined by a point and a direction vector
        (_, bisectrix) = intersectLines(
            vertices[i], b,     # line of bisectrix
            vertices[iPrev],    # side of triangle
            vertices[iNext] - vertices[iPrev]
        )
        bisectrixes.append(bisectrix)

    # A circle center is an intersection of 2 bisectrixes
    (_, center) = intersectLines(
        vertices[0], bisectrixes[0] - vertices[0],
        vertices[1], bisectrixes[1] - vertices[1]
    )
    # The circle radius equals to the distance from the center
    # to the first side of triangle
    radius = center.distanceToLine(
        vertices[0], vertices[1] - vertices[0]
    )
    return (center, radius, bisectrixes)

if __name__ == "__main__":
    main()
