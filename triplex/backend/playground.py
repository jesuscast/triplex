import collections
import os
import json

cleanNameSector = "Biotechnology"
#cleanNameSector = ''.join(ch for ch in stocks_n_sector[stock_id][1] if ch.isalnum())
graphRange = 130

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

stockData = stockFromFiles("BTE")
#---- get the averages price of the sector
inFF = open(path+"/triplex/backend/download_data/sectors_organized/"+cleanNameSector+".txt","r")
sector_avg = json.loads(inFF.read())
inFF.close()
ordered_sector = collections.OrderedDict(sorted(sector_avg.items(), key=lambda t: int(t[0])))
ordered_stock = collections.OrderedDict(sorted(stockData.items(), key=lambda t: int(t[0])))
initialTime_sector = 0
initialTime_sector_index = 0
initialTime_stock = ordered_stock.keys()[0]
initialPriceSector = 0
for i, timeSector in enumerate(ordered_sector):
	if initialTime_stock > int(timeSector):
		continue
	else:
		initialTime_sector = int(timeSector)
		initialTime_sector_index = i
		break


finalTime_sector = 0
finalTime_sector_index = 0
finalTime_stock = ordered_stock.keys()[::-1][0]
prices_sector = []
for i, timeSector in enumerate(ordered_sector):
	if finalTime_stock > int(timeSector):
		continue
	else:
		finalTime_sector = int(timeSector)
		finalTime_sector_index = i
		break


interval = int ( int( finalTime_sector_index - initialTime_sector_index )/float(graphRange) )
valsForComparison = []
timesToCalculate = []
currentInterval = 0
for i, key in enumerate(ordered_sector):
	if i < initialTime_sector_index:
		continue
	if i%interval==0:
		currentInterval += 1
	else:
		continue
	valsForComparison.append(ordered_sector[key])
	timesToCalculate.append((int(key)-initialTime_sector)/60)

[ (int(n)-initialTime_stock)/60  for n in ordered_sector.keys() ]
[ i*interval for i,n in enumerate(timesToCalculate) ]
enumerate()
# times_stock = timesToCalculate
# times_sector = timesToCalculate
# [(i, ordered_stock[n][3]) for i, n in enumerate(ordered_stock)]
# prices_stock = getY(zip(ordered_stock.keys() , [ordered_stock[n][3] for n in ordered_stock]), timesToCalculate)
# print prices_stock
# prices_sector = valsForComparison
# changesStock = []
# changesSector = []

prices_stock = valsForComparison
for i, price in enumerate(prices_stock):
	if i==0:
		continue
	else:
		changesSector.append(float(prices_sector[i])/float(prices_sector[0]))
		changesStock.append(float(prices_stock[i])/float(prices_stock[0]))


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
return {'times':times_stock, 'changes':changes, 'prices':prices_stock}



raw_data_string = ""
	total_number_stocks = len(stocks_r)
	for i in range(stocks_r):
		# i holds the stock number
		len_of_this_stock = len(stocks_r[i])
		string_of_this_stock = ""
		for j, k in enumerate(stocks_r[i]):
			#k holds the timestamp
			string_of_this_price = str(k)+","
			string_of_this_price += ",".join([ str(n) for n in stocks_r[i][k] ])
			if(j!=(len_of_this_stock-1)):
				string_of_this_stock += "^"
		if(i!=(total_number_stocks-1)):
			raw_data_string += "###"


raw_data_string = ""
total_number_stocks = len(stocks_r)
for i in range(stocks_r):
	# i holds the stock number
	len_of_this_stock = len(stocks_r[i])
	string_of_this_stock = ""
	for j, k in enumerate(stocks_r[i])
		#k holds the timestamp
		string_of_this_price = str(k)+","
		string_of_this_price += ",".join([ str(n) for n in stocks_r[i][k] ])
		if(j!=(len_of_this_stock-1)):
			string_of_this_stock += "^"
	if(i!=(total_number_stocks-1)):
		raw_data_string += "###"

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




