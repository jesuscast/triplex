#imports
#########################################
import bottle
import yahoostocks as ys
import datetime
import random
import numpy as np
#Global variables
#########################################
app = bottle.Bottle()

#Functions
#########################################

#Route the JS files
@app.route('/js/<js_file>')
def server_static_js(js_file):
	return bottle.static_file(js_file, root='js')

#Route the CSS files
@app.route('/css/<css_file>')
def server_static_css(css_file):
	return bottle.static_file(css_file, root='css')

#Route the latest realtime stocks from today
@app.route('/realtimestock/<stock_id>')
def retrieveStock(stock_id):
	data = ys.realtime(stock_id)
	rawtimes = [float(n[0]) for n in data]
	times = [datetime.datetime.fromtimestamp(n) for n in rawtimes]
	times = [((n.hour*60+n.minute-60*9)/3) for n in times]
	minT = min(times)
	x_axis = [str(n-minT) for n in times]
	close_prices = [float(n[1]) for n in data]
	maxP = max(close_prices)
	minP = min(close_prices)
	range_prices = (maxP-minP)/130
	y_axis = [str((n-minP)/range_prices) for n in close_prices]
	alpha_values =[float(i) for i in range(0,len(x_axis))]
	maxA = max(alpha_values)
	minA = min(alpha_values)
	range_alpha = (maxA-minA)/130
	z_axis = [str((n-minA)/range_alpha) for n in alpha_values]
	#rows = ["%s,%s,%s"%(x_axis[i], y_axis[i], z_axis[i]) for i in range(len(data))]
	rows = []
	rows.append(",".join(x_axis))
	rows.append(",".join(y_axis))
	rows.append(",".join(z_axis))
	return "\n".join(rows)

#Route the latest realtime stocks from today and put axis in the specific coordinates bro
@app.route('/realtimestocks/<stocks_id>')
def retrieveStocks(stocks_id):
	stocks = stocks_id.split(",")
	result = ""
	data = []
	maxP = 0
	minP = 100000
	# maxA = 0
	# minA = 0
	range_prices = 0
	range_alpha = 0
	stocksLength = len(stocks)
	for i, stock in enumerate(stocks):
		data.append(ys.realtime(stock))
		#data[i]
	for i in range(stocksLength):
		for j in range(len(data[i])):
			temp = float(data[i][j][1])
			if temp > maxP:
				maxP = temp
			if temp < minP:
				minP = temp
	minP -= 50
	range_prices = (maxP-minP+100)/130
	# result = str(minP)+" "+str(maxP)+" "+str(range_prices)+"\n"
	for i in range(stocksLength):
		rawtimes = [float(n[0]) for n in data[i]]
		times = [datetime.datetime.fromtimestamp(n) for n in rawtimes]
		times = [((n.hour*60+n.minute-60*9)/3) for n in times]
		minT = min(times)
		x_axis = [str(n-minT) for n in times]
		close_prices = [float(n[1]) for n in data[i]]
		y_axis = [str((n-minP)/range_prices) for n in close_prices]
		alpha_values =[float(i) for i in range(0,len(x_axis))]
		maxA = max(alpha_values)
		minA = min(alpha_values)
		range_alpha = (maxA-minA)/130
		z_axis = [str((n-minA)/range_alpha) for n in alpha_values]
		rows = []
		rows.append(",".join(x_axis))
		rows.append(",".join(y_axis))
		rows.append(",".join(z_axis))
		result += "\n".join(rows) +"^"
	return result


#Route the latest realtime stocks from today and put axis in the specific coordinates bro
@app.route('/retrievesector/<stocks_id>')
def retrieveSector(stocks_id):
	stocksList = stocks_id.split(',')
	stocks = []
	processedData = []
	changesZ = []
	maxP = 0.0
	minP = 100000.0
	minT = 0
	stocksLength = len(stocksList)
	shortestStockIndex = 0
	rangePrices = 0.0
	for i, stock in enumerate(stocksList):
		stocks.append(ys.realtime(stock))
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
		xAxis = []
		yAxis = []
		processedData.append({})
		processedData[i]['x'] = []
		processedData[i]['y'] = []
		processedData[i]['z'] = []
		changesZ.append([])
		changesZ[i].append(0)
		for j in range(len(stocks[i])):
			thisTime = datetime.datetime.fromtimestamp(float(stocks[i][j][0]))
			xAxis.append(str(((thisTime.hour*60+thisTime.minute-60*9)/3)-minT))
			yAxis.append(str((float(stocks[i][j][1])-minP)/rangePrices))
			if j!=0:
				changesZ[i].append(\
					float(stocks[i][j][1])-\
					float(stocks[i][j-1][1])\
					)
			# the following avoids retrieving stocks from the last hours
			# if float(xAxis[len(xAxis)-1]) >= 130.0:
			# 	break
		changesZ[i][0] = changesZ[i][1]
		processedData[i]['x'] = xAxis
		processedData[i]['y'] = yAxis
	for j in range(1, len(stocks[shortestStockIndex])):
		tot = 0.0
		for i in range(len(stocks)):
			tot += float(changesZ[i][j])
		#print tot+","
		for i in range(len(stocks)):
			if (changesZ[i][j] != 0) and (tot != 0):
				processedData[i]['z'].append(\
					str(changesZ[i][j]/tot*130)\
					)
				#print processedData[i][j][-1]
			else:
				# processedData[i]['z'][(len(processedData[i]['z'])-1)]
				processedData[i]['z'].append(str(processedData[i]['z'][(len(processedData[i]['z'])-1)]))
	return '^'.join([','.join(stock['x'])+"\n"+','.join(stock['y'])+"\n"+','.join(stock['z']) for stock in processedData])
	

@app.route('/retrievesectorhistorical/<stocks_id>')
def retrieveSectorHistorical(stocks_id):
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
		stocks.append(ys.historical(stock, {'month':1, 'day': 1, 'year':1990},{'month':1, 'day': 1, 'year':2014}))
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
	for j in range(1, len(stocks[shortestStockIndex])):
		tot = 0.0
		for i in range(len(stocks)):
			tot += float(changesZ[i][j])
		#print tot+","
		for i in range(len(stocks)):
			if (changesZ[i][j] != 0) and (tot != 0):
				processedData[i]['z'].append(\
					str(changesZ[i][j]/tot*130)\
					)
				#print processedData[i][j][-1]
			else:
				# processedData[i]['z'][(len(processedData[i]['z'])-1)]
				processedData[i]['z'].append(str(0.0))
	return '^'.join([','.join(stock['x'])+"\n"+','.join(stock['y'])+"\n"+','.join(stock['z']) for stock in processedData])


#Retrieves the stocks xyz axis using a polynomial fit
@app.route('/stocks-xyz/<stocks_id>')
def retrieveSectorHistorical(stocks_id):
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
	for j in range(1, len(stocks[shortestStockIndex])):
		tot = 0.0
		#modified version
		smallestChange = 1000.0
		biggestChange = 0.0
		minZ = 0.0
		maxZ = 130.0
		sign = 1
		#modified version
		for i in range(len(stocks)):
			tot += float(changesZ[i][j])
		if tot<0.0:
			sign = sign*-1
		for i in range(len(stocks)):
			if smallestChange > changesZ[i][j]/tot:
				smallestChange = changesZ[i][j]/tot
			if biggestChange < changesZ[i][j]/tot:
				biggestChange = changesZ[i][j]/tot
		print smallestChange
		print biggestChange
		#print tot+","
		for i in range(len(stocks)):
			if (changesZ[i][j] != 0) and (tot != 0):
				processedData[i]['z'].append(\
					str(sign*changesZ[i][j]*(maxZ-minZ)/(biggestChange-smallestChange))\
					)
				#print processedData[i][j][-1]
			else:
				# processedData[i]['z'][(len(processedData[i]['z'])-1)]
				processedData[i]['z'].append(str(0.0))

	#for i in range(len(processedData)):
		#make fit
		# ztemporal = []
		# xtemporal = []
		# if len(processedData[i]['z']) > len(processedData[i]['x']):
		# 	ztemporal = np.array([ float(processedData[i]['z'][j]) for j in range(len(processedData[i]['x'])) ])
		# 	xtemporal = np.array([ float(n) for n in processedData[i]['x'] ])
		# else:
		# 	xtemporal = np.array([ float(processedData[i]['x'][j]) for j in range(len(processedData[i]['z'])) ])
		# 	ztemporal = np.array([ float(n) for n in processedData[i]['z']])

		# # do fit
		# M = np.column_stack((xtemporal**2,)) # construct design matrix
		# k, _, _, _ = np.linalg.lstsq(M, ztemporal) # least-square fit of M * k = y

		# # equationFit = np.polyfit(xtemporal, ztemporal, 1)
		# # equation = np.poly1d(equationFit)
		# lol = k*xtemporal**2
		# resultEquation = lol[0:len(lol)-1]
		# processedData[i]['z'] = [ str(n) for n in resultEquation]
		# processedData[i]['z'] = [ str(equation(xValue)) for xValue in xtemporal]

	return '^'.join([','.join(stock['x'])+"\n"+','.join(stock['y'])+"\n"+','.join(stock['z']) for stock in processedData])

#Route main page
@app.route('/')
def hello():
	return bottle.static_file("graphingModule.html", root="")
	#return "HELLO FAKA"


#Init calls
#########################################
bottle.run(app, host="localhost", port=8080, debug=True)