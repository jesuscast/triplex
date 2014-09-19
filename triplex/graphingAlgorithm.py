stocksList = stocksString.split("")
stocks = []
processedData = []
changesZ = []
maxP = 10000.0
minP = 0.0
stocksLength = len(stocksList)
shortestStockIndex = 0
rangePrices = 0.0
for i, stock in enumerate(stocksList):
	stocks.append(ys.realtime(stock))
for i in range(stocksLength):
	if len(stocks[shortestStockIndex]) > len(stocks[i]):
		shortestStockIndex = i
	for j in range(len(stocks[i])):
		temp = float(stocks[i][j][1])
		if temp > maxP:
			maxP = temp
		if temp < minP:
			minP = temp
				