import requests
import json
import os

#This function cleans up the screen
def cls():
    os.system(['clear','cls'][os.name == 'nt'])



timePeriod1 = "633820948" # 1/31/1990  21h 22min 28sec GMT
timePeriod2 = "1422738308" # Sat, 31 Jan 2015 21:05:08 GMT
wrong = u"\u2717" #unicode symbol for X mark for wrong answers
right = u"\u2713" #unicode symbol for check mark for right answers
rightN = 0
wrongN = 0

json_data = open("stock_symbols.json","r")
symbols = json.loads(json_data.read())
perOne = (len(symbols)-len(symbols)%100)/100
print perOne
seconds = 2.58*len(symbols)
minutes = 0
hours = 0
totalTimeString = ""
if seconds > 60:
	minutes = (seconds-seconds%60)/60
	seconds = seconds-minutes*60
	if minutes > 60:
		hours = (minutes-minutes%60)/60
		minutes = minutes-hours*60



def refreshScreen(index, percentage, rr, ww):
	cls()
	successRate = rr/index
	print(str(index/percentage)+"%  Percentage with "+str(successRate)+"%  Success Rate")
	print right*int(index/percentage)

totalTimeString = str(hours)+" Hours "+str(minutes)+" minutes and "+str(seconds)+" seconds"
print(totalTimeString)
answer = raw_input("Do you want to continue? (y/n)")
start = perOne
if answer =="y":
	i = 0
	for key_i in symbols:
		#in order to skip the ones that we already downloaded
		if i<start:
			i+=1
			continue
		stock_name = str(symbols[key_i])
		headers = {
			"Accept":"*/*",
			"Accept-Encoding":"gzip, deflate, sdch",
			"Accept-Language":"en-US,en;q=0.8,es;q=0.6,fr;q=0.4",
			"Connection":"keep-alive",
			"Content-Type":"application/json",
			"Cookie":"V=v=0.7&m=1&ccOptions=%7B%22show%22%3Afalse%2C%22lang%22%3A%22en%22%2C%22fontSize%22%3A24%2C%22fontName%22%3A%22Helvetica%20Neue%2CHelvetica%2CArial%2C_sans%22%2C%22fontColor%22%3A%22%23ffffff%22%2C%22fontOpacity%22%3A1%2C%22fontEffect%22%3A%22none%22%2C%22bgColor%22%3A%22%23000000%22%2C%22bgOpacity%22%3A0.75%7D; AO=u=1; B=45ao6bpa75a7h&b=4&d=t3Cgg95pYFo0kLO2COaSFA--&s=v8&i=xqogd0CxVg34lI1X0jz.; F=a=wPQtWV0MvSzWOfdi7xEFKF2a.FwQki_.x2d22XRSKutz5wOk9flLeJO6bRVAHeHRVrPqYLI-&b=gLp9; PH=fn=Skgk5bXmqx7maH3KS1nc&l=en-US&i=us; ywandp=1000911397279%3A916720109; fpc=1000911397279%3AZc8fB2pf%7C%7C; PRF=&t=GOOG",
			"Host":"finance.yahoo.com",
			"Referer":"http://finance.yahoo.com/echarts?s="+stock_name+"+Interactive",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36",
			"X-Requested-With":"XMLHttpRequest"
		}
		url = "http://finance.yahoo.com/_td_charts_api/resource/charts"+\
				";comparisonTickers="+\
				";events=div|split|earn"+\
				";gmtz=-5"+\
				";indicators=quote"+\
				";period1="+timePeriod1+\
				";period2="+timePeriod2+\
				";queryString={\"s\":\""+stock_name+"+Interactive\"}"+\
				";range=1d"+\
				";rangeSelected=undefined"+\
				";ticker="+stock_name+\
				";useMock=false?crumb=%2FNnXZqZT%2Fpi"
		request = requests.get(url = url, headers = headers)
		if request.status_code == requests.codes.ok:
			result_file = open(stock_name+".txt","w")
			result_file.write(request.text)
			result_file.close()
			rightN += 1
		else:
			wrongN += 1
		if(i%perOne==0):
			refreshScreen(i, perOne, rightN, wrongN)
		i+=1
else:
	print "OK bye"
