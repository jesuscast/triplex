def sectorBezier(stocks_id):
	'''
	x,y,z = 0,1,2
	'''
	#---- separate the list of stocks
	stocksList = stocks_id.split(',')
	#---- set Variables
	maxP = -10000.0
	minP = 100000.0
	#---- initiate Variables
	stocks = []
	processedData = []
	changesZ = []
	stocksLength = len(stocksList)
	shortestStockIndex = 0
	rangePrices = 0.0
	graphRange = 130.0
	#---- retrieve stocks information
	for stock in stocksList:
		stocks.append(ys.historical(stock, {'month':1, 'day': 1, 'year':2014},{'month':1, 'day': 20, 'year':2014}))
	#---- find the limits of the stocks so the x, y, and z axis match in length for all stocks
	#---- this also finds the extrema for the prices so we could normalize the graph
	for i in range(stocksLength):
		if len(stocks[shortestStockIndex])>len(stocks[i]):
			shortestStockIndex = i
		for j in range(len(stocks[i])):
			temp = float(stocks[i][j][1])
			if temp > maxP:
				maxP = temp
			if temp < minP:
				minP = temp
	# minP -= 50
	print "shortestStockIndex:"+str(shortestStockIndex)
	#---- now that we have the shortestStockIndex we can set a limits to normalize the x axis
	minT = 0.0
	maxT = float(len(stocks[shortestStockIndex]))
	axisLimit = int(maxT)
	rangePrices = graphRange/(maxP-minP)
	rangeT = graphRange/(maxT-minT)
	print "maxT:"+str(maxT)
	#---- creates the axis values
	for i in range(stocksLength):
		#---- initialize variables
		xAxis = []
		yAxis = []
		processedData.append([])
		processedData[i].append([])
		processedData[i].append([])
		processedData[i].append([])
		changesZ.append([])
		changesZ[i].append(0)
		for j in range(axisLimit):
			#thisTime = datetime.datetime.fromtimestamp(float(stocks[i][j][0]))
			#xAxis.append(str(((thisTime.hour*60+thisTime.minute-60*9)/3)-minT))
			if j!=0:
				xAxis.append(rangeT*float(j))
			else:
				xAxis.append((0.0))
			yAxis.append(((float(stocks[i][j][1])-minP)*rangePrices))
			if j!=0:
				changesZ[i].append(\
					float(stocks[i][j][1])-\
					float(stocks[i][0][1])\
					)
			# ---- the following avoids retrieving stocks from the last hours
			# if float(xAxis[len(xAxis)-1]) >= 130.0:
			# 	break
		print "changesZ length:"+str(len(changesZ[i]))
		changesZ[i][0] = changesZ[i][1]
		processedData[i][0] = xAxis
		processedData[i][1] = yAxis
	print printList(changesZ)
	#--- calcualtes the changes in prices
	for j in range(1, axisLimit):
		tot = 0.0
		for i in range(stocksLength):
			tot += float(changesZ[i][j])
		print "tot:"+str(tot)
		for i in range(stocksLength):
			if (changesZ[i][j] != 0) and (tot != 0):
				print "inside if"
				processedData[i][2].append(\
					float(changesZ[i][j]/tot)\
					)
			else:
				# processedData[i]['z'][(len(processedData[i]['z'])-1)]
				if i>0:
					processedData[i][2].append((processedData[i][2][-1]))
					print "tot=0 or changes=0"
				else:
					processedData[i][2].append(0.0)
					print "zero here"
	print printList(processedData)
	#---- normalizes the data in the z axis
	minZProcessed = 10000.0
	maxZProcessed = -10000.0
	#----finds the limits for the z axis normalization
	for i in range(stocksLength):
		for j in range(axisLimit-1):
			if float(processedData[i][2][j]) < minZProcessed:
				minZProcessed = float(processedData[i][2][j])
			if float(processedData[i][2][j]) > maxZProcessed:
				maxZProcessed = float(processedData[i][2][j])
	if maxZProcessed == minZProcessed:
		maxZProcessed = graphRange
		minZProcessed = 0.0
	print "maxZ:"+str(maxZProcessed)
	print "minZ:"+str(minZProcessed)
	rangeZ = graphRange/(maxZProcessed-minZProcessed)
	for i in range(stocksLength):
		for j in range(axisLimit-1):
			processedData[i][2][j] = ((float(processedData[i][2][j])-minZProcessed)*rangeZ)
		#---- repeats the last value so we don't miss anything
		processedData[i][2].append(processedData[i][2][-1])
	print printList(processedData)
	return '^'.join([','.join(stock[0])+"%"+','.join(stock[1])+"%"+','.join(stock[2]) for stock in valsInString(processedData)])