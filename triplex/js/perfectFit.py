x = 0
def getY(points, pointsRequested):
	lPoints = len(points)
	newPoints = []
	#---- it is really important to declare the lastI and index right here
	lastI = 0
	index = 0
	for x in pointsRequested:
		if lPoints>1:
			ended = False
			for i in range(lastI, lPoints):
				if ended==False:
					if x > points[i][0]:
						print "x:"+str(x)+" points[i][0]:"+str(points[i][0])
						index = i
						#---- this prevents the code from going again to this index
						lastI = index+1
						print "index:"+str(index)+" value:"+str(points[index][1])
						ended = True
			if index+2 <= lPoints:
				slope = (points[index+1][1]-points[index][1])/(points[index+1][0]-points[index][0])
				print "index:"+str(index)
				print "slope:"+str(slope)
				if slope<0:
					print "slope negative"
				else:
					print "slope is positive"
				b = points[index][1]-slope*points[index][0]
				newPoints.append(x*slope+b)
	return newPoints


getY([(1,12),(2,4),(3,0)],[2.3,1.2,2.7])

getY(zip(r3[0],r3[1]),newXAxis)

curve = bezier.Curve()
curve.draw(zip(r3[0], r3[2]), 100)
newZAxis = [ n[1] for n in curve.result ]
newXAxis = [ n[0] for n in curve.result ]
newYAxis = getY(zip(r3[0],r3[1]), newXAxis)
finalAxis.append([newXAxis, newYAxis, newZAxis])