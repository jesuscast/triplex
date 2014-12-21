#imports
#########################################
import bottle
import yahoostocks as ys
import datetime
import random
<<<<<<< HEAD
=======

>>>>>>> a20a3a77320cf046579caffff1d740e950de19cb
import algorithmStocks as algorithmStocks
import webbrowser
#Global variables
#########################################
app = bottle.Bottle()
webbrowser.open("http://localhost:8080")

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

@app.route('/images/<images_file>')
def server_static_css(images_file):
	return bottle.static_file(images_file, root='images')

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

#Retrieves the stocks xyz axis using a polynomial fit
@app.route('/stocks-xyz/<stocks_id>')
def yodude(stocks_id):
	return algorithmStocks.sectorBezier(stocks_id)

@app.route('/returnarray')
def yodude():
	return [1,2,3,[4,23,[123,213,123,123,123]]]

#Route main page
@app.route('/')
def hello():
	return bottle.static_file("graphingModule.html", root="")
	#return "HELLO FAKA"


#Init calls
#########################################
bottle.run(app, host="localhost", port=8080, debug=True)