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
	stocks = []
	processedData = []
	#changesZ = []
	stocksLength = len(stocksList)
	shortestStockIndex = 0
	rangePrices = 0.0
	graphRange = 130.0
	rangeChanges = 0.0
	#---- retrieve stocks information
	for stock in stocksList:
		stocks.append(stock_in_sector(stock, fromDate, toDate))
	#---- find the limits of the stocks so the x, y, and z axis match in length for all stocks
	#---- this also finds the extrema for the prices so we could normalize the graph
	for i in range(stocksLength):
		if len(stocks[shortestStockIndex])>len(stocks[i]):
			shortestStockIndex = i
		for j in range(len(stocks[i]['prices'])):
			temp = stocks[i]['prices'][j]
			if temp > maxP:
				maxP = temp
			if temp < minP:
				minP = temp
			#calculate the range in changes
			tempC = stocks[i]['changes'][j]
			if tempC > maxC:
				maxC = temp
			if tempC < minC:
				minC = tempC

	# minP -= 50
	# print "shortestStockIndex:"+str(shortestStockIndex)
	#---- now that we have the shortestStockIndex we can set a limits to normalize the x axis
	minT = 0.0
	maxT = float(len(stocks[shortestStockIndex]))
	axisLimit = int(maxT)
	rangePrices = graphRange/(maxP-minP)
	rangeChanges = graphRange/(maxC-minC)
	rangeT = graphRange/(maxT-minT)
	# print "maxT:"+str(maxT)
	#---- creates the axis values
	for i in range(stocksLength):
		#---- initialize variables
		xAxis = []
		yAxis = []
		zAxis = []
		processedData.append([])
		processedData[i].append([])
		processedData[i].append([])
		processedData[i].append([])
		for j in range(axisLimit):
			#thisTime = datetime.datetime.fromtimestamp(float(stocks[i][j][0]))
			#xAxis.append(str(((thisTime.hour*60+thisTime.minute-60*9)/3)-minT))
			if j!=0:
				xAxis.append(rangeT*float(j))
			else:
				xAxis.append((0.0))
			zAxis.append( (stocks[i]['prices'][j] - minP) *rangePrices))
			yAxis.append( (stocks[i]['changes'][j] - minC)*rangeChanges)
		processedData[i][0] = xAxis
		processedData[i][1] = yAxis
		processedData[i][2] = zAxis
	# print # printList(processedData)
	#---- create new values using bezier curve
	finalAxis = []
	for i in range(len(processedData)):
		curve = bezier.Curve()
		curve.draw(zip(processedData[i][0],processedData[i][2]), 100)
		newZAxis = [ n[1] for n in curve.result ]
		newXAxis = [ n[0] for n in curve.result ]
		newYAxis = getY(zip(processedData[i][0],processedData[i][1]), newXAxis)
		finalAxis.append([newXAxis, newYAxis, newZAxis])
	#---- normalizes the data in the z axis
	#---- the r are for eliminating the crazy extrema
	minZProcessed = 10000.0
	maxZProcessed = -10000.0
	maxPProcessed = -10000.0
	minPProcessed = 10000.0
	finalAxisLength = len(finalAxis)
	finalAxisZLength = len(finalAxis[0][2])
	#---- finds the limits for the z axis normalization
	for i in range(finalAxisLength):
		for j in range(finalAxisZLength):
			if float(finalAxis[i][2][j]) < minZProcessed:
				minZProcessed = float(finalAxis[i][2][j])
			if float(finalAxis[i][2][j]) > maxZProcessed:
				maxZProcessed = float(finalAxis[i][2][j])
	if maxZProcessed == minZProcessed:
		maxZProcessed = 1.0
		minZProcessed = 0.0
	# print "maxZ:"+str(maxZProcessed)
	# print "minZ:"+str(minZProcessed)
	rangeZ = graphRange/(maxZProcessed-minZProcessed)
	for i in range(finalAxisLength):
		for j in range(finalAxisZLength):
			finalAxis[i][2][j] = ((float(finalAxis[i][2][j])-minZProcessed)*rangeZ)
	#---- finds the limits for the y axis normalization
	for i in range(finalAxisLength):
		for j in range(finalAxisZLength):
			if float(finalAxis[i][1][j]) < minPProcessed:
				minPProcessed = float(finalAxis[i][1][j])
			if float(finalAxis[i][1][j]) > maxPProcessed:
				maxPProcessed = float(finalAxis[i][1][j])
	if maxPProcessed == minPProcessed:
		maxPProcessed = 1.0
		minPProcessed = 0.0
	rangePProcessed = graphRange/(maxPProcessed-minPProcessed)
	for i in range(finalAxisLength):
		for j in range(finalAxisZLength):
			finalAxis[i][1][j] = ((float(finalAxis[i][1][j])-minPProcessed)*rangePProcessed)
	#---- repeats the last value so we don't miss anything
	# finalAxis[i][2].append(processedData[i][2][-1])
	# print # printList(processedData)
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
	#lol = "^".join([",".join(n) for n in [ [str(n) for n in k] for k in stocks]])
	return lol+"-MAXIMUMSEPARATOR-"+'^'.join([','.join(stock[0])+"%"+','.join(stock[1])+"%"+','.join(stock[2]) for stock in valsInString(finalAxis)])


def stock_in_sector(stock_id, fromDateR, toDateR):
	#---- separate the list of stocks
	fromDate = [ int(n) for n in fromDateR.split(',') ]
	toDate = [ int(n) for n in toDateR.split(',') ]
	#---- initiate Variables
	stockData = []
	#---- retrieve stocks information
	stockData = ys.historical(stock, {'month':fromDate[1], 'day': fromDate[0], 'year':fromDate[2]},{'month':toDate[1], 'day': toDate[0], 'year':toDate[2]})[::-1]
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
