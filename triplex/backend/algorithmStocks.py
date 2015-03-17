import yahoostocks as ys
import types
import bezier
import time
import datetime
import json
import os
import collections

path = os.getcwd()
inF = open(path+"/triplex/backend/download_data/stocks_and_their_sector.json","r")
stocks_n_sector = json.loads(inF.read())
inF.close()
print "lllll"

def stockFromFiles(stock_id):
	pathT = os.getcwd().replace("triplex-code","download_data/historical_prices/")
	stockF = open(pathT+stock_id+".txt","r")
	stockJ = json.loads(stockF.read())
	stockF.close()
	finalF = {}
	for i in range(len(stockJ[u'data'][u'timestamp'])):
		#finalF.append([])
		finalF[stockJ[u'data'][u'timestamp'][i]]=[stockJ[u'data'][u'indicators'][u'quote'][0][u'open'][i], stockJ[u'data'][u'indicators'][u'quote'][0][u'high'][i], stockJ[u'data'][u'indicators'][u'quote'][0][u'low'][i], stockJ[u'data'][u'indicators'][u'quote'][0][u'close'][i], stockJ[u'data'][u'indicators'][u'quote'][0][u'volume'][i]]
	return finalF

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


def valsInString(listCurrent):
	result = []
	if type(listCurrent) is not types.ListType:
		## print listCurrent
		return str(listCurrent)
	else:
		for thisSubList in listCurrent:
			## print thisSubList
			result.append(valsInString(thisSubList))
		return result


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


def valsInFloat(listCurrent):
	result = []
	if type(listCurrent) is not types.ListType:
		## print listCurrent
		return float(listCurrent)
	else:
		for thisSubList in listCurrent:
			## print thisSubList
			result.append(valsInFloat(thisSubList))
		return result


def stringStocksToList(stocksString):
	return valsInFloat([ [ k.split(",") for k in n.split("%")] for n in stocksString.split("^") ])


def sectorBezier(stocks_id, fromDateR, toDateR):
	'''
	x,y,z = 0,1,2
	fromDate = day, month, year
	toDate = day, month, year

	[times, changes, prices]
	'''
	#---- separate the list of stocks
	stocksList = stocks_id.split(',')
	fromDate = [ int(n) for n in fromDateR.split(',') ]
	toDate = [ int(n) for n in toDateR.split(',') ]
	#---- set Variables
	maxP = -10000.0
	minP = 100000.0
	minC = 10000.0
	maxC = -10000.0
	#---- initiate Variables
	stocksRaw = []
	stocks = []
	stocks_r = []
	#changesZ = []
	stocksLength = len(stocksList)
	shortestStockIndex = 0
	rangePrices = 0.0
	graphRange = 130.0
	rangeChanges = 0.0
	#---- retrieve stocks information
	#---- just draw the curve
	for stock in stocksList:
		stockR = stockFromFiles(stock)
		stockT  = stock_in_sector(stock, stockR)
		stocksRaw.append(stockR)
		curve = bezier.Curve()
		timesAll = range(len(stockT['times']))
		#print ",".join([ str(n) for n in times ])
		#return "----p"+str(stockT['prices'][0])+"q--"
		curve.draw(zip(timesAll,stockT['changes']), len(stockT['times']))
		xAxis = [ n[0] for n in curve.result ]
		yAxis = [ n[1] for n in curve.result ]
		zAxis = getY(zip(timesAll,stockT['prices']), xAxis)
		stocks_r.append([xAxis, yAxis, zAxis])
		# print "xAxis:"
		# print xAxis
		# print "yAxis:"
		# print yAxis
		# print "zAxis:"
		# print zAxis
	#--- Normalize
	#--Normalize Prices and changes
	shortestStockIndex = 0
	for i, stock in enumerate(stocks_r):
		tempP = max(stock[2])
		if maxP < tempP:
			maxP = tempP
		tempP_m = min(stock[2])
		if minP > tempP_m:
			minP = tempP_m
		tempC = max(stock[1])
		if maxC < tempC:
			maxC = tempC
		tempC_m = min(stock[1])
		if minC > tempC_m:
			minC = tempC_m
		if len(stocks_r[shortestStockIndex]) > len(stock):
			shortestStockIndex = i

	minT = 0.0
	maxT = float(len(stocks_r[shortestStockIndex]))
	axisLimit = int(maxT)
	rangePrices = graphRange/(maxP-minP)
	rangeChanges = graphRange/(maxC-minC)
	rangeT = graphRange/(maxT-minT)

	for i, stock in enumerate(stocks_r):
		stocks.append([])
		stocks[i] = []
		stocks[i].append( stock[0] )
		stocks[i].append( [ (n-minC)*rangeChanges for n in stock[1] ] )
		stocks[i].append( [ (n-minP)*rangePrices for n in stock[2] ] )
	lol = ""
	lenI = len(stocks)
	for i in range(lenI):
		tempStrJ = ""
		lenJ = len(stocks[i])
		for j in range(lenJ):
			tempStr = ""
			lenK = len(stocks[i][j])
			for k in range(lenK):
				tempStr += str(stocks[i][j][k])
				if(k!=(lenK-1)):
					tempStr += ","
			tempStrJ += tempStr
			if(j!=(lenJ-1)):
				tempStrJ += "^"
		lol += tempStrJ
		if(i!=(lenI-1)):
			lol += "###"
	final_string = lol+"-MAXIMUMSEPARATOR-"+'^'.join([','.join(stock[0])+"%"+','.join(stock[1])+"%"+','.join(stock[2]) for stock in valsInString(stocks)])
	print final_string
	return final_string
def stock_in_sector(stock_id, stockData):
	cleanNameSector = ''.join(ch for ch in stocks_n_sector[stock_id][1] if ch.isalnum())
	graphRange = 130
	#---- get the averages price of the sector
	inFF = open(path+"/triplex/backend/download_data/sectors_organized/"+cleanNameSector+".txt","r")
	sector_avg = json.loads(inFF.read())
	inFF.close()
	sector_avg = { int(n):sector_avg[n] for n in sector_avg }
	ordered_sector = collections.OrderedDict(sorted(sector_avg.items(), key=lambda t: int(t[0])))
	ordered_stock_r = collections.OrderedDict(sorted(stockData.items(), key=lambda t: int(t[0])))
	ordered_stock = collections.OrderedDict()
	for k in ordered_stock_r:
		ordered_stock[k] = ordered_stock_r[k][3]

	graphRange = 130
	perOne = len(ordered_stock)/130
	prices_stock = []
	prices_sector = []
	times = []
	for i, n in enumerate(ordered_stock):
		if i%perOne != 0:
			continue
		if ordered_stock[n] != None and ordered_sector[n] !=None:
			times.append(n)


	changesStock = []
	changesSector = []

	for i, time in enumerate(times):
		if i==0:
			continue
		else:
			changesSector.append(float(ordered_sector[time])/float(ordered_sector[times[0]]))
			changesStock.append(float(ordered_stock[time])/float(ordered_stock[times[0]]))
	changes = []
	for j in range(0, len(changesStock)):
		if (changesStock[j] > changesSector[j]) and changesStock[j] > 0 and changesSector > 0:
			changes.append(changesStock[j] / changesSector[j])
		elif (changesStock[j] < changesSector[j]) and changesStock[j] > 0 and changesSector > 0:
			changes.append(- changesSector[j] / changesStock[j])
		elif changesStock[j] > changesSector[j] and changesStock[j] < 0 and changesSector[j] < 0:
			#negative over negative becomes positive
			changes.append(changesSector[j] / changesStock[j])
		elif changesStock[j] < changesSector[j] and changesStock[j] < 0 and changesSector[j] < 0:
			changes.append(- changesStock[j] / changesSector[j])
		elif changesStock[j] > changesSector[j] and changesStock[j] > 0 and changesSector[j] < 0:
			changes.append(changesStock[j] / (changesStock[j] - changesSector[j]))
		elif changesStock[j] < changesSector[j] and changesStock[j] < 0 and changesSector[j] > 0:
			changes.append(- changesSector[j] / (changesSector[j] - changesStock[j]))
	return {'times':times, 'changes':changes, 'prices':[ ordered_stock[n] for n in times ]}
