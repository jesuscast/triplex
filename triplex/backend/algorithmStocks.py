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

def stockFromYahoo(stock='GOOG', from_date={'month':1, 'day': 1, 'year':2014}, to_date={'month':-1}):
	result = ys.historical(stock, from_date, to_date)[::-1]
	final = {}
	for i, price in enumerate(result):
		timeS = int(time.mktime(datetime.datetime.strptime(price[0], "%Y-%m-%d").timetuple()))
		final[timeS] = [ float(n) for i, n in enumerate(price) if i!=0 ]
	return final

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
	stocks = []
	stocks_r = []
	stocksRaw = []
	#changesZ = []
	stocksLength = len(stocksList)
	shortestStockIndex = 0
	rangePrices = 0.0
	graphRange = 130.0
	rangeChanges = 0.0
	#---- retrieve stocks information
	#---- just draw the curve
	for j, stock in enumerate(stocksList):
		stockR = stockFromYahoo(stock, {'month':fromDate[1], 'day': fromDate[0], 'year':fromDate[2]},{'month':toDate[1], 'day': toDate[0], 'year':toDate[2]} )
		stockT  = stock_in_sector(stock, stockR)
		curve = bezier.Curve()
		timesAll = range(len(stockT['times']))
		#print stockT
		# import sys
		# sys.exit()
		#print ",".join([ str(n) for n in times ])
		#return "----p"+str(stockT['prices'][0])+"q--"
		curve.draw(zip(timesAll,stockT['changes']), len(stockT['times']))
		xAxis = [ n[0] for n in curve.result ]
		yAxis = [ n[1] for n in curve.result ]
		zAxis = getY(zip(timesAll,stockT['prices']), xAxis)
		stocks_r.append([xAxis, yAxis, zAxis])
		stocksRaw.append([])
		for i, time in enumerate(stockT['times']):
			stocksRaw[j].append([])
			stocksRaw[j][i].append(int(time))
			for val in stockR[time]:
				stocksRaw[j][i].append(val)
			stocksRaw[j][i].append(yAxis[i])
		#print stocks_r
	#print stocksRaw
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
		if len(stocks_r[shortestStockIndex][0]) > len(stock[0]):
			shortestStockIndex = i

	if minC > 0:
		minC = 0.0
	if maxC < 0:
		maxC = 0.0
	minT = 0.0
	maxT = float(len(stocks_r[shortestStockIndex][0]))
	#print "maxT:"+str(maxT)+", min "+str(minT)+", range "+str(graphRange/float((maxT-minT)))
	rangePrices = graphRange/(maxP-minP)
	rangeChanges = graphRange/(maxC-minC)
	rangeT = graphRange/float((maxT-minT))

	for i, stock in enumerate(stocks_r):
		stocks.append([])
		stocks[i] = []
		stocks[i].append( [ (n)*rangeT for n in stock[0] ])
		stocks[i].append( [ (n-minC)*rangeChanges for n in stock[1] ] )
		stocks[i].append( [ (n-minP)*rangePrices for n in stock[2] ] )
	
	raw_data_string = ""
	lenStocks_r = len(stocksRaw)
	for i in range(lenStocks_r):
		# i holds the index of the current stock
		lenStocks_r_vals = len(stocksRaw[i])
		string_of_this_stock = ""
		for j in range(lenStocks_r_vals):
			#j holds the index of the current element in the stock
			string_of_this_stock += ",".join( [ str(n) for n in stocksRaw[i][j] ] )
			if(j != (lenStocks_r_vals-1)):
				string_of_this_stock += "^"
		raw_data_string += string_of_this_stock
		if(i!=(lenStocks_r-1)):
			raw_data_string += "###"

	origin = str(0.0)+","+str(round(-minC*rangeChanges, 2))+","+str(round(minP*rangePrices,2))
	final_string = raw_data_string+"-MAXIMUMSEPARATOR-"+'^'.join([','.join(stock[0])+"%"+','.join(stock[1])+"%"+','.join(stock[2]) for stock in valsInString(stocks)])+"-MAXIMUMSEPARATOR-"+origin
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
	if perOne > 0:
		for i, n in enumerate(ordered_stock):
			if i%perOne != 0:
				continue
			if n in ordered_stock and n in ordered_sector:
				if ordered_stock[n] != None and ordered_sector[n] !=None:
					times.append(n)
	else:
		for i, n in enumerate(ordered_stock):
			if n in ordered_stock and n in ordered_sector:
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
