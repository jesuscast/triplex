#iterates for creating the precision

#NECESSARY FUNCTIONS

#FLOAT STEP
from __future__ import division
from math import log

def xfrange(start, stop, step):

    old_start = start #backup this value

    digits = int(round(log(10000, 10)))+1 #get number of digits
    magnitude = 10**digits
    stop = int(magnitude * stop) #convert from 
    step = int(magnitude * step) #0.1 to 10 (e.g.)

    if start == 0:
        start = 10**(digits-1)
    else:
        start = 10**(digits)*start

    data = []   #create array

    #calc number of iterations
    end_loop = int((stop-start)//step)
    if old_start == 0:
        end_loop += 1

    acc = start

    for i in xrange(0, end_loop):
        data.append(acc/magnitude)
        acc += step

    return data
#END FLOAT STEP
#END NECESSARY FUNCTIONS

#FUNCTIONS
def drawCurve(pointsArray, pointNumber):
	if len(pointsArray)==1:
		zAxisCurve.append((pointsArray[0][0],pointsArray[0][1]))
	else:
		newPoints = []
		for i in range(0, len(pointsArray)-1):
			x = (1-pointNumber) * pointsArray[pointNumber][0] + t * pointsArray[pointNumber+1][0]
			y = (1-pointNumber) * pointsArray[pointNumber][1] + t * pointsArray[pointNumber+1][1]
			newPoints.append((x,y))
		drawCurve(newPoints, pointNumber)
#END FUNCTIONS

#SETS VARIABLES
maxZ = 300.0
minZ = 0.0
precision = 300.0
xAxis = [1,2,3]
yAxis = [3,4,5]
points = zip(xAxis, yAxis)
zAxisCurve = []
#END SET VARIABLES

t = 0.0
step = (maxZ-minZ)/precision
for pointN in xfrange(minZ,maxZ+step,step):
	drawCurve(points, pointN)

#end iterates for creating the precision