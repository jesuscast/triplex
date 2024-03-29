import yahoostocks as ys
import types

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