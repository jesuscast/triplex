#imports
#########################################
import os
import bottle
from backend import yahoostocks as ys
import datetime
import random
from backend import algorithmStocks as algorithmStocks
from backend import realtimeStocks as realtimeStocks
import webbrowser

#Global variables
#########################################
bottle.debug(True)
app = bottle.Bottle()
webbrowser.open("http://localhost:8080")

#Functions
#########################################

def path_to(name_of_file):
	dir = os.path.dirname(__file__)
	filename = os.path.join(dir, name_of_file)
	return str(filename)

#Route the JS files
@app.route('/js/<js_file>')
def server_static_js(js_file):
	return bottle.static_file(js_file, root=path_to('frontend/js'))

#Route the CSS files
@app.route('/css/<css_file>')
def server_static_css(css_file):
	return bottle.static_file(css_file, root=path_to('frontend/css'))

@app.route('/images/<images_file>')
def server_static_css(images_file):
	return bottle.static_file(images_file, root=path_to('frontend/images'))

#Route the latest realtime stocks from today and put axis in the specific coordinates bro
@app.route('/realtimestocks/<stocks_id>')
def realtime():
	return realtimeStocks.retrieveStocks(stocks_id)

#Retrieves the stocks xyz axis using a polynomial fit
@app.route('/stocks-xyz/<stocks_id>')
def yodude(stocks_id):
	return algorithmStocks.sectorBezier(stocks_id, bottle.request.query.fromDate, bottle.request.query.toDate)

#Route main page
@app.route('/')
def hello():
	return bottle.static_file("graphingModule.html", root=path_to('frontend'))


#Init calls
#########################################
bottle.run(app, host="localhost", port=8080, debug=True)
