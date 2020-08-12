from tkinter import *
from R2Graph import *

def main():
    rootWindow = Tk()
    rootWindow.title("Triangle")
    rootWindow.geometry("800x600")

    points = []

    panel = Frame(rootWindow)
    drawArea = Canvas(rootWindow, bg="lightBlue")

    def clear():
        drawArea.delete("all")
        points.clear()

    clearButton = Button(panel, text="Clear", command=clear)

    def drawTriangle():
        if len(points) >= 3:
            drawArea.create_line(
                points[0].x, points[0].y,
                points[1].x, points[1].y,
                points[2].x, points[2].y,
                points[0].x, points[0].y,
                fill="blue", width=2
            )
            (centers, radiuses, bisectrixes, tangents, nagel) = inCircle(points)
            for i in range(3):
                center = centers[i]
                radius = radiuses[i]
                # Draw an inscribed circle
                drawArea.create_oval(
                    center.x - radius, center.y - radius,
                    center.x + radius, center.y + radius,
                    fill="", outline="red", width=2
                )
                # Draw the center of circle
                drawArea.create_oval(
                    center.x - 4, center.y - 4,
                    center.x + 4, center.y + 4,
                    fill="red", outline="red"
                )
                # Draw the tangent points
                drawArea.create_oval(
                    tangents[i].x - 4, tangents[i].y - 4,
                    tangents[i].x + 4, tangents[i].y + 4,
                    fill="red", outline="red"
                )
            # Draw the Nagel point
            drawArea.create_oval(
                nagel.x - 4, nagel.y - 4,
                nagel.x + 4, nagel.y + 4,
                fill="black", outline="black"
            )                
            # Draw bisectrixes and for nagel point
            for i in range(3):
                drawArea.create_line(
                    points[i].x, points[i].y,
                    2 * points[i].x - bisectrixes[i].x, 2 * points[i].y - bisectrixes[i].y,
                    fill="darkGreen", width=1
                )
                drawArea.create_line(
                    points[i].x, points[i].y,
                    bisectrixes[i].x, bisectrixes[i].y,
                    fill="darkGreen", width=1
                )
                iPrev = i - 1
                if iPrev < 0:
                    iPrev = 2
                iNext = i + 1
                if iNext >= 3:
                    iNext = 0
                drawArea.create_line(
                    tangents[i].x, tangents[i].y,
                    points[iNext].x, points[iNext].y,
                    fill="darkGreen", width=1
                )
                drawArea.create_line(
                    points[i].x, points[i].y,
                    points[i].x + 3 * (points[i].x - points[iPrev].x), points[i].y + 3 * (points[i].y - points[iPrev].y),
                    fill="yellow", width=1
                )
                drawArea.create_line(
                    points[i].x, points[i].y,
                    points[i].x + 3 * (points[i].x - points[iNext].x), points[i].y + 3 * (points[i].y - points[iNext].y),
                    fill="yellow", width=1
                )
    drawButton = Button(panel, text="Draw", command=drawTriangle)

    panel.pack(fill=X, padx=4, pady=4)
    clearButton.pack(side=LEFT)
    drawButton.pack(side=LEFT)
    drawArea.pack(fill=BOTH, side=TOP, expand=True, padx=4, pady=4)

    def onButtonPress(e):
        if len(points) >= 3:
            clear()
        points.append(R2Point(e.x, e.y))
        drawArea.create_line(
            e.x - 8, e.y, e.x + 8, e.y, fill="red", width=3
        )
        drawArea.create_line(
            e.x, e.y-8, e.x, e.y+8, fill="red", width=3
        )

    drawArea.bind("<Button-1>", onButtonPress)

    rootWindow.mainloop()

# Compute bisectrixes of triangle and 
# a center & radius of inscribed circle
def inCircle(vertices):
    centers = []
    radiuses = []
    bisectrixes = []
    tangents = []
    
    for i in range(3):
        iPrev = i - 1
        if iPrev < 0:
            iPrev = 2
        iNext = i + 1
        if iNext >= 3:
            iNext = 0
        vPrev = (vertices[iPrev] - vertices[i]).normalized()
        vNext = (vertices[iNext] - vertices[i]).normalized()
        
        b = vNext - vPrev   # The direction vector of i-th bisectrix
        # The point of bisectrix is calculated as intersection of 2 lines,
        # where a line is defined by a point and a direction vector
        (_, bisectrix) = intersectLines(
                vertices[i], b,     # line of bisectrix
                vertices[iPrev],    # side of triangle
                vertices[iPrev] - vertices[iNext]
        )
        bisectrixes.append(bisectrix)  
                
    for i in range(3):
        iCurr = i
        iPrev = i - 1
        if iPrev < 0:
            iPrev = 2
        # A circle center is an intersection of 2 bisectrixes
        (_, center) = intersectLines(
            vertices[iPrev], bisectrixes[iPrev] - vertices[iPrev],
            vertices[iCurr], bisectrixes[iCurr] - vertices[iCurr]
        )
        centers.append(center)
        #tangent point
        (_, tangent) = intersectLines(
            vertices[iPrev], vertices[iCurr] - vertices[iPrev],
            center, (vertices[iCurr] - vertices[iPrev]).normal()
        )
        tangents.append(tangent)
        # The circle radius equals to the distance from the center
        # to the first side of triangle
        radius = center.distanceToLine(
            vertices[iPrev], vertices[iCurr] - vertices[iPrev]
        )
        radiuses.append(radius)
    #Nagel point
    (_, nagel) = intersectLines(
        tangents[1], vertices[2] - tangents[1],
        tangents[2], vertices[0] - tangents[2],
    )    
    return (centers, radiuses, bisectrixes, tangents, nagel)

if __name__ == "__main__":
    main()
