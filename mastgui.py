# @Author: johnhaigh
# @Date:   2020-11-13T18:12:16+00:00
# @Last modified by:   johnhaigh
# @Last modified time: 2020-11-15T23:41:06+00:00

# Location and bearing calculations areuse code based on MoveableType.com's work in Javascript, re-written in Python
# Antenna angle reference data from US Department of Science field antenna handbook 1984


from tkinter import *
import math
import string
from math import pi
from trianglesolver import *

window = Tk()

def gridDistance(transmitgrid, receivegrid):

    # Convert to fully numeric references
    p1 = gridrefNumeric(transmitgrid)
    p2 = gridrefNumeric(receivegrid)

    # Get E/N distances between ref1 & ref2
    deltaE = int(p2[0])-int(p1[0])
    deltaN = int(p2[1])-int(p1[1])

    # Pythagoras gives us the distance between the points
    distance = math.sqrt(deltaE*deltaE + deltaN*deltaN)

    # Return distance in KM, rounded
    distance = round(distance/100, 2)

    return distance
def gridBearing(transmitgrid, receivegrid):

    # Convert to fully numeric references
    p1 = gridrefNumeric(transmitgrid)
    p2 = gridrefNumeric(receivegrid)

    # Get E/N distances between ref1 & ref2
    deltaE = int(p2[0])-int(p1[0])
    deltaN = int(p2[1])-int(p1[1])

    # Arctan gives us the bearing, just need to convert -pi..+pi to 0..360 deg
    deg = (90-(math.atan2(deltaN, deltaE)/math.pi*180)+360) % 360
    mils = round(deg * 17.777778, 2)

    return mils
def gridrefNumeric(gridref):

    #get numeric values of letter references, mapping A->0, B->1, C->2, etc:
    letE = (ord(gridref[0].upper())-(ord('A')))
    letN = (ord(gridref[1].upper())-(ord('A')))

    #shuffle down letters after 'I' since 'I' is not used in grid:
    if letE > 7:
        letE -= 1
    if (letN > 7):
        letN -= 1

    # Convert grid letters into 100km-square indexes from false origin (grid square SV)
    e = ((letE+3)%5)*5 + (letN%5)
    n = (19-math.floor(letE/5)*5) - math.floor(letN/5)

    #skip grid letters to get numeric part of ref
    gridref = gridref[2:]

    #append numeric part of references to grid index:
    e = str(e) + gridref[4:]
    n = str(n) + gridref[:4]

    return e, n
def anglecalcday (distance):

    dist = distance

    if 0 <= dist <= 80:
        angleday = 90
    elif 81 <= dist <= 153:
        angleday = 80
    elif 154 <= dist <= 258:
        angleday = 70
    elif 259 <= dist <= 403:
        angleday = 60
    elif 404 <= dist <= 443:
        angleday = 50
    elif 444 <= dist <= 564:
        angleday = 45
    elif 565 <= dist <= 644:
        angleday = 40
    elif 645 <= dist <= 725:
        angleday = 35
    elif 726 <= dist <= 966:
        angleday = 30
    elif 967 <= dist <= 1127:
        angleday = 25
    elif 1128 <= dist <= 1450:
        angleday = 20
    elif 1451 <= dist <= 1932:
        angleday = 15
    elif 1933 <= dist <= 2415:
        angleday = 10
    elif 2415 <= dist <= 3200:
        angleday = 5
    else :
        angleday = 0

    return angleday
def anglecalcnight (distance):

    dist = distance

    if 0 <= dist <= 145:
        anglenight = 90
    elif 146 <= dist <= 290:
        anglenight = 80
    elif 291 <= dist <= 443:
        anglenight = 70
    elif 444 <= dist <= 685:
        anglenight = 60
    elif 686 <= dist <= 805:
        anglenight = 50
    elif 806 <= dist <= 966:
        anglenight = 45
    elif 967 <= dist <= 1127:
        anglenight = 40
    elif 1128 <= dist <= 1328:
        anglenight = 35
    elif 1329 <= dist <= 1610:
        anglenight = 30
    elif 1611 <= dist <= 1328:
        anglenight = 25
    elif 1329 <= dist <= 1610:
        anglenight = 20
    elif 1611 <= dist <= 1771:
        anglenight = 15
    elif 1772 <= dist <= 2254:
        anglenight = 10
    elif 2255 <= dist <= 2898:
        anglenight = 5
    else :
        anglenight = 0

    return anglenight

window.title("Mast Calculator")

# Top Title
titletop = Label(window, text="Mast Calculator\n\nSimple calulator for determining the angle, direction and length of antenna required")
titletop.grid(columnspan=6, row=0, pady=40)

# Label for freq entry window
lbl = Label(window, text="Enter frequency")
lbl.grid(column=1, row=2)

txt = Entry(window)
txt.grid(column=2, row=2, columnspan=2, pady=5)

commenttxt1 = Label(window, text="Format X,XXX Mhz")
commenttxt1.grid(column=4, row=2)

# Sending grid
lblgrid1 = Label(window, text="Enter send grid")
lblgrid1.grid(column=1, row=3)

grid1 = Entry(window)
grid1.grid(column=2, row=3, columnspan=2, pady=5)

commentgrid1 = Label(window, text="8 figure grid")
commentgrid1.grid(column=4, row=3)

# Reciving grid
lblgrid2 = Label(window, text="Enter receiving grid")
lblgrid2.grid(column=1, row=4)

grid2 = Entry(window)
grid2.grid(column=2, row=4, columnspan=2, pady=5)

commentgrid2 = Label(window, text="e.g. SN12345678")
commentgrid2.grid(column=4, row=4)

# Antenna type available
lblgrid2 = Label(window, text="Antenna type available")
lblgrid2.grid(column=0, row=5, pady=5)

antennalen = IntVar()
antennalen.set(1)

Radiobutton(window, text="Cut to length", variable=antennalen, value=5).grid(column = 1, row = 5)
Radiobutton(window, text="Vehicle BB", variable=antennalen, value=24).grid(column = 2, row = 5)
Radiobutton(window, text="Patrol BB 8m", variable=antennalen, value=8).grid(column = 3, row = 5)
Radiobutton(window, text="Patrol BB 16m", variable=antennalen, value=16).grid(column = 4, row = 5)
Radiobutton(window, text="Patrol BB 32m", variable=antennalen, value=32).grid(column = 5, row = 5)

# Mast type label
lblgrid2 = Label(window, text="Mast type available")
lblgrid2.grid(column=0, row=6, pady=5)

mast = IntVar()
mast.set(1)

Radiobutton(window, text="Patrol Mast / 5.4m", variable=mast, value=5).grid(column = 1, row = 6)
Radiobutton(window, text="8m Mast", variable=mast, value=8).grid(column = 2, row = 6)
Radiobutton(window, text="12m Mast", variable=mast, value=11).grid(column = 3, row = 6)

# Define function on click of braid submit button
def click():

    if antennalen.get() != 5:

        length = antennalen.get()
        antennalength = str(length)

    else:

        frequency = float(txt.get())
        if frequency >= 1.6 and frequency <= 29.9999:
            clansman = 68.5
            length = round(float(clansman / frequency),1)
            antennalength = str(length)

    # Run calculations to create direction and angle values
    transmitgrid = grid1.get()
    receivegrid = grid2.get()
    distance = gridDistance(transmitgrid, receivegrid)
    bearing = round(gridBearing(transmitgrid, receivegrid))

    angleday = anglecalcday(distance)
    anglenight = anglecalcnight(distance)

    # Print distance
    distanceresult = Label(window, text="Distance of transmission: " + str(distance) + "km")
    distanceresult.grid(columnspan = 3, row=9, column=0)

    # Print bearing
    bearingresult = Label(window, text="Use bearing: " + str(bearing) + "mils")
    bearingresult.grid(columnspan = 3, row=9, column=3)

    # Print angle day
    angleresult = Label(window, text="Angle of send during day: "+ str(angleday) + " degrees")
    angleresult.grid(columnspan = 3, row=11, column=0, pady=10)

    # Print angle night
    angleresult = Label(window, text="Angle of send night: " + str(anglenight) + " degrees")
    angleresult.grid(columnspan = 3, row=11, column=3, pady=10)

    # Calcute elevation height required to acheive angle during day

    a = solve(c=length, C=90*degree, B=angleday*degree)
    string = 0

    maxmast = mast.get()

    # Calculate the amount of additonal length is required to make up that angle
    # For cut to length variable antenna
    if antennalen.get() == 5:

        while a[0] < float(maxmast):
            # Supplement with string until maxmast value can be acheived
            string = string + .1
            a = solve(c=(length+string), C=90*degree, B=angleday*degree)

    # For cut to broadban fixed length antenna
    else:

        while a[0] < float(maxmast):

            a = solve(c=(length), C=90*degree, B=angleday*degree)

    triangleday = Label(window, text= "Antenna elevated to: " + str(round(a[0], 2)) + "m\n\n" + "Braid length: " + antennalength + "m\n\n" + "Additional string required: " + str(round(string, 2)) + "m" )
    triangleday.grid(columnspan = 3, row=12, column=0)

    # Calcute elevation height required to acheive angle during day
    a = solve(c=length, C=90*degree, B=anglenight*degree)
    string = 0

    # Calculate the amount of additonal length is required to make up that angle
    # For cut to length variable antenna
    if antennalen.get() == 5:

        while a[0] < float(maxmast):
            # Supplement with string until maxmast value can be acheived
            string = string + .1
            a = solve(c=(length+string), C=90*degree, B=anglenight*degree)

    # For cut to broadban fixed length antenna
    else:

        while a[0] < float(maxmast):

            a = solve(c=(length), C=90*degree, B=anglenight*degree)

    trianglenight = Label(window, text= "Antenna elevated to: " + str(round(a[0], 2)) + "m\n\n" + "Braid length: " + antennalength + "m\n\n" + "Additional string required: " + str(round(string, 2)) + "m" )
    trianglenight.grid(columnspan = 3, row=12, column=3)

# Submit information and trigger def method

btn = Button(window, text="Calculate", command=click)
btn.grid(columnspan=6, row=7,pady=20)

txt.focus()
window.mainloop()
