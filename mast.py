# @Author: johnhaigh
# @Date:   2020-11-10T11:12:48+00:00
# @Last modified by:   johnhaigh
# @Last modified time: 2020-11-15T23:44:35+00:00

# Location and bearing calculations areuse code based on MoveableType.com work in Javascript, re-written in Python
# Reference data from US Department of Science field antenna handbook 1984

import math
import string
import tkinter as tk

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


frequency = input("Enter frequency: ")
frequency = float(frequency)

if frequency >= 1.6 and frequency <= 29.9999:

    clansman = 68.5
    length = round(float(clansman / frequency),1)

print(f"Length of braid required is: ",length,"m")

transmitgrid = input("Enter 8 figure grid reference where you are: ")
receivegrid = input("Enter 8 figure grid reference of patrol: " )
distance = gridDistance(transmitgrid, receivegrid)
bearing = round(gridBearing(transmitgrid, receivegrid))

angleday = anglecalcday(distance)
anglenight = anglecalcnight(distance)

print(f"\nDistance between two points is: ",distance,"km")
print(f"\nBearing is: ",bearing,"mils")
print(f"\nTakeoff angle:")
print(f"      Daytime: ", angleday,"degrees")
print(f"      Nighttime: ", anglenight,"degrees")
print("\n")
