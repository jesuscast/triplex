#Retrieves the stocks xyz axis using a polynomial fit
@app.route('/stocks-xyz-bezier/<stocks_id>')
def sectorBezier(stocks_id):
	stocksList = stocks_id.split(',')
	stocks = []
	processedData = []
	changesZ = []
	maxP = 0.0
	minP = 100000.0
	stocksLength = len(stocksList)
	shortestStockIndex = 0
	rangePrices = 0.0
	for i, stock in enumerate(stocksList):
		# stocks.append(ys.historical(stock))
		stocks.append(ys.historical(stock, {'month':1, 'day': 1, 'year':2014},{'month':1, 'day': 20, 'year':2014}))
		# data[i]
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
	rangePrices = (maxP-minP)/130.0
	# return str(minP)+" "+str(maxP)+" "+str(rangePrices)
	for i in range(len(stocks)):
		minT = 0.0	
		maxT = float(len(stocks[i]))
		print maxT
		rangeT = (maxT-minT)/130.0
		xAxis = []
		yAxis = []
		processedData.append({})
		processedData[i]['x'] = []
		processedData[i]['y'] = []
		processedData[i]['z'] = []
		changesZ.append([])
		changesZ[i].append(0)
		for j in range(len(stocks[i])):
			#thisTime = datetime.datetime.fromtimestamp(float(stocks[i][j][0]))
			#xAxis.append(str(((thisTime.hour*60+thisTime.minute-60*9)/3)-minT))
			if j!=0:
				xAxis.append(str(float(j)/float(rangeT)))
			else:
				xAxis.append(str(0))
			yAxis.append(str((float(stocks[i][j][1])-minP)/rangePrices))
			if j!=0:
				changesZ[i].append(\
					float(stocks[i][j][1])-\
					float(stocks[i][0][1])\
					)
			# the following avoids retrieving stocks from the last hours
			# if float(xAxis[len(xAxis)-1]) >= 130.0:
			# 	break
		changesZ[i][0] = changesZ[i][1]
		processedData[i]['x'] = xAxis
		processedData[i]['y'] = yAxis

	#range for changes

	# smallestChange = 1000.0
	# biggestChange = 0.0
	# currentValue = 0.0
	# minZ = 0.0
	# maxZ = 130.0

	# for i in range(len(changesZ)):
	# 	for j in range(len(changesZ[i])):
	# 		if smallestChange > changesZ[i][j]:
	# 			smallestChange = changesZ[i][j]
	# 		if biggestChange < changesZ[i][j]:
	# 			biggestChange = changesZ[i][j]

	#rqange for changes end

	#calculates the z axis 1
	# for j in range(1, len(stocks[shortestStockIndex])):
	# 	tot = 0.0
	# 	#modified version
	# 	smallestChange = 1000.0
	# 	biggestChange = 0.0
	# 	minZ = 0.0
	# 	maxZ = 130.0
	# 	sign = 1
	# 	#modified version
	# 	for i in range(len(stocks)):
	# 		tot += float(changesZ[i][j])
	# 	if tot<0.0:
	# 		sign = sign*-1
	# 	for i in range(len(stocks)):
	# 		if smallestChange > changesZ[i][j]/tot:
	# 			smallestChange = changesZ[i][j]/tot
	# 		if biggestChange < changesZ[i][j]/tot:
	# 			biggestChange = changesZ[i][j]/tot
	# 	print "smallestChange:"+str(smallestChange)
	# 	print "biggestChange:"+str(biggestChange)
	# 	#print tot+","
	# 	for i in range(len(stocks)):
	# 		if (changesZ[i][j] != 0) and (tot != 0):
	# 			processedData[i]['z'].append(\
	# 				str(sign*changesZ[i][j]*(maxZ-minZ)/(biggestChange-smallestChange))\
	# 				)
	# 			#print processedData[i][j][-1]
	# 		else:
	# 			# processedData[i]['z'][(len(processedData[i]['z'])-1)]
	# 			processedData[i]['z'].append(str(0.0))
	#end calculates the z axis 1

	#calcualtes the z axis
	for j in range(1, len(stocks[shortestStockIndex])):
		tot = 0.0
		for i in range(len(stocks)):
			tot += float(changesZ[i][j])
		for i in range(len(stocks)):
			if (changesZ[i][j] != 0) and (tot != 0):
				processedData[i]['z'].append(\
					float(changesZ[i][j]/tot*130.0)\
					)
			else:
				# processedData[i]['z'][(len(processedData[i]['z'])-1)]
				processedData[i]['z'].append((processedData[i]['z'][(len(processedData[i]['z'])-1)]))
	#end calculates the z axis

	# normalization of the z axis
	minZProcessed = 10000.0
	maxZProcessed = -10000.0
	graphRange = 130.0
	for i in range(len(processedData)):
		for j in range(len(processedData[i]['z'])):
			if float(processedData[i]['z'][j]) < minZProcessed:
				minZProcessed = float(processedData[i]['z'][j])
			if float(processedData[i]['z'][j]) > maxZProcessed:
				maxZProcessed = float(processedData[i]['z'][j])
	if maxZProcessed == minZProcessed:
		maxZProcessed = graphRange
		minZProcessed = 0.0
	print "max:"+str(maxZProcessed)
	print "min"+str(minZProcessed)
	rangeZ = graphRange/(maxZProcessed-minZProcessed)
	for i in range(len(processedData)):
		for j in range(len(processedData[i]['z'])):
			processedData[i]['z'][j] = str((float(processedData[i]['z'][j])-minZProcessed)*rangeZ)
		processedData[i]['z'].append(processedData[i]['z'][-1])
	#end normalizartion

	# for i in range(len(processedData)):
	# 	# make fit
	# 	ztemporal = []
	# 	xtemporal = []
	# 	if len(processedData[i]['z']) > len(processedData[i]['x']):
	# 		ztemporal = np.array([ float(processedData[i]['z'][j]) for j in range(len(processedData[i]['x'])) ])
	# 		xtemporal = np.array([ float(n) for n in processedData[i]['x'] ])
	# 	else:
	# 		xtemporal = np.array([ float(processedData[i]['x'][j]) for j in range(len(processedData[i]['z'])) ])
	# 		ztemporal = np.array([ float(n) for n in processedData[i]['z']])

	# 	# do fit
	# 	M = np.column_stack((xtemporal**2,)) # construct design matrix
	# 	k, _, _, _ = np.linalg.lstsq(M, ztemporal) # least-square fit of M * k = y

	# 	# equationFit = np.polyfit(xtemporal, ztemporal, 1)
	# 	# equation = np.poly1d(equationFit)
	# 	lol = k*xtemporal**2
	# 	resultEquation = lol[0:len(lol)-1]
	# 	processedData[i]['z'] = [ str(n) for n in resultEquation]
		# processedData[i]['z'] = [ str(equation(xValue)) for xValue in xtemporal]

	#start bezier
	for i in range(len(processedData)):
		curve = bezier.Curve()
		curve.draw([(float(processedData[i]['x'][j]),float(processedData[i]['z'][j])) for j in range(len(processedData[i]['x']))], len(processedData[i]['x']))
		processedData[i]['z'] = [str(n) for n in curve.result]
	#end bezier

	return '^'.join([','.join(stock['x'])+"\n"+','.join(stock['y'])+"\n"+','.join(stock['z']) for stock in processedData])