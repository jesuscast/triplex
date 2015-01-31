import newyahoostocks as ys
import types
import bezier
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
						# print "x:"+str(x)+" points[i][0]:"+str(points[i][0])
						index = i
						#---- this prevents the code from going again to this index
						lastI = index+1
						# print "index:"+str(index)+" value:"+str(points[index][1])
						ended = True
			if index+2 <= lPoints:
				slope = (points[index+1][1]-points[index][1])/(points[index+1][0]-points[index][0])
				# print "index:"+str(index)
				# print "slope:"+str(slope)
				# if slope<0:
				# 	# print "slope negative"
				# else:
				# 	# print "slope is positive"
				b = points[index][1]-slope*points[index][0]
				newPoints.append(x*slope+b)
	return newPoints


def valsInString(currentVal):
	#print(type(a))
	if type(currentVal) not in [types.DictType, types.ListType]:
		#print "is not a dict"
		#print "this transformed to string is "+str(a)
		return str(currentVal)
	elif type(currentVal) is types.DictType:
		#print "it is a dict"
		r = {}
		for key in currentVal:
			#print "this is a value with key "+key
			#print a[key]
			r[str(key)]=valsInString(currentVal[key])
		#print(r)
		return r
	elif type(currentVal) is types.ListType:
		r = []
		for thisSubList in currentVal:
			## print thisSubList
			r.append(valsInString(thisSubList))
		return r

def printList(listCurrent, depth=0):
	result = ""
	if type(listCurrent) is not types.ListType:
		## print listCurrent
		return "--"*depth+str(depth)+":"+str(listCurrent)+"\n"
	else:
		for i, thisSubList in enumerate(listCurrent):
			## print thisSubList
			result += "--"*depth+str(depth)+":element #"+str(i)+"\n"
			result +=(printList(thisSubList, depth+1))
		return result



def stringStocksToList(stocksString):
	return valsInFloat([ [ k.split(",") for k in n.split("%")] for n in stocksString.split("^") ])


#def (stocks_id, fromDateR, toDateR):

def getSectorHistorical():
	rawData = valsInString(ys.sectorData())
	close_prices = rawData['data']['indicators']['quote'][0]['close']
	times = rawData['data']['timestamp']
	return r


#lol
"""
lol.keys()
['debug', 'isValidRange', 'data', 'isLegacy']
>>> lol['debug']
'Host: pprd3-node2521-lh1.manhattan.gq1.yahoo.com'
>>> lol['isValidRange']
'True'
>>> lol['isLegacy']
'False'
>>>
loll = lol['data']

len(loll) = 3

loll.keys()
['indicators', 'timestamp', 'meta']

type(loll['indicators'])
lolll = loll['indicators']['quote']
lolll.keys()

loll['indicators'].keys()
['quote']


type(lol['data']['indicators']['quote'][0].keys())
lol['data']['indicators']['quote'][0].keys()
['high', 'volume', 'open', 'low', 'close']
lol['data']['indicators']['quote'][0]['close']

len(lol['data']['indicators']['timestamp'])
"""