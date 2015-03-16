import yahoostocks as ys
import types
import bezier
import time
import datetime
import json

inF = open("download_data/stocks_and_their_sector.json","r")
stocks_n_sector = json.loads(inF.read())
inF.close()

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
	processedData = []
	#changesZ = []
	stocksLength = len(stocksList)
	shortestStockIndex = 0
	rangePrices = 0.0
	graphRange = 130.0
	rangeChanges = 0.0
	#---- retrieve stocks information
	#---- just draw the curve
	for stock in stocksList:
		stockR = ys.historical(stock, {'month':fromDate[1], 'day': fromDate[0], 'year':fromDate[2]},{'month':toDate[1], 'day': toDate[0], 'year':toDate[2]})[::-1]
		stockT  = stock_in_sector(stock, fromDate, toDate, stockR))
		stocksRaw.append(stockR)
		curve = bezier.Curve()
		times = range(len(stockT['times']))
		curve.draw(zip(times,stockT['changes']), 100)
		xAxis = [ n[0] for n in curve.result ]
		yAxis = [ n[1] for n in curve.result ]
		zAxis = getY(zip(times,stockT['prices']), xAxis)
		stocks.append([xAxis, yAxis, zAxis])
	#---- find the limits of the stocks so the x, y, and z axis match in length for all stocks
	#---- this also finds the extrema for the prices so we could normalize the graph
	for i in range(stocksLength):
		if len(stocks[shortestStockIndex])>len(stocks[i]):
			shortestStockIndex = i
		for j in range(len(stocks[i][0])):
			temp = stocks[i][2][j]
			if temp > maxP:
				maxP = temp
			if temp < minP:
				minP = temp
			#calculate the range in changes
			tempC = stocks[i][1][j]
			if tempC > maxC:
				maxC = temp
			if tempC < minC:
				minC = tempC

	minT = 0.0
	maxT = float(len(stocks[shortestStockIndex]))
	axisLimit = int(maxT)
	rangeChanges = graphRange/(maxC-minC)
	rangePrices = graphRange/(maxP-minP)
	rangeT = graphRange/(maxT-minT)

	for i in range(len(stocks)):
		for j in range(len(stocks[i][0])):
			stocks[i][0][j] = stocks[i][0][j] * rangeT
			stocks[i][1][j] = (stocks[i][1][j]-minC)*rangeChanges
			stocks[i][2][j] = (stocks[i][2][j]-minP)*rangePrices

	origin = [0.0, -minC*rangeChanges][(minC<0.0)==True]
	lol = ""
	lenI = len(stocksRaw)
	for i in range(lenI):
		tempStrJ = ""
		lenJ = len(stocksRaw[i])
		for j in range(lenJ):
			tempStr = ""
			lenK = len(stocksRaw[i][j])
			for k in range(lenK):
				tempStr += str(stocksRaw[i][j][k])
				if(k!=(lenK-1)):
					tempStr += ","
			tempStrJ += tempStr
			if(j!=(lenJ-1)):
				tempStrJ += "^"
		lol += tempStrJ
		if(i!=(lenI-1)):
			lol += "###"
	#lol = "^".join([",".join(n) for n in [ [str(n) for n in k] for k in stocks]])
	return lol+"-MAXIMUMSEPARATOR-"+'^'.join([','.join(stock[0])+"%"+','.join(stock[1])+"%"+','.join(stock[2]) for stock in valsInString(stocks)])+"-MAXIMUMSEPARATOR-"+str(origin)


def stock_in_sector(stock_id, fromDate, toDate, stockData):
	#---- separate the list of stocks
	#---- initiate Variables
	stockData = []
	#---- retrieve stocks information
	#---- substitute the first date for the timestamp
	#--- results
	changes = []
	prices = []
	times = []
	for i in range(0, len(stockData)):
		#timestamp
		stockData[i][0] = int(time.mktime(datetime.datetime.strptime(stockData[i][0], "%Y-%m-%d").timetuple()))
		#open
		stockData[i][1] = float(stockData[i][1])
		#high
		stockData[i][2] = float(stockData[i][2])
		#low
		stockData[i][3] = float(stockData[i][3])
		#close
		stockData[i][4] = float(stockData[i][4])
		#volume
		stockData[i][5] = int(stockData[i][5])
		#adjVolume
		stockData[i][6] = float(stockData[i][6])
	#---- find the stock in the sectors
	#sector = stocks_n_sector[stock_id][1]
	cleanNameSector = ''.join(ch for ch in stocks_n_sector[stock_id][1] if ch.isalnum())
	#---- get the averages price of the sector
	inFF = open("download_data/sectors_organized/"+cleanNameSector+".txt","r")
	sector_avg = json.loads(inFF.read())
	inFF.close()
	#---- try to create the motherfucking axis

	initialTime = 1
	initialPriceStock = 1
	initialPriceSector = 1
	changesStock = []
	changesSector = []
	i = 0
	for price_stock in stockData:
		timeHere = price_stock[0]
		if str(timeHere) in sector_avg:
			if i==0:
				initialTime = timeHere
				initialPriceStock = price_stock[4]
				initialPriceSector = float(sector_avg[timeHere])
			else:
				changesSector.append(float(sector_avg[str(timeHere)])/initialPriceSector)
				changesStock.append(price_stock[4]/initialPriceStock)
				prices.append(price_stock[4])
				times.append(price_stock[0])
			i += 1
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

	return {'times':times, 'changes':changes, 'prices':prices}
