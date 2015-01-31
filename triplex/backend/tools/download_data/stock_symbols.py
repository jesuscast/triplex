import requests
import json
import re
import bs4
import types

def valsInString(currentVal):
	#print(type(a))
	if type(currentVal) not in [types.DictType, types.ListType]:
		#print "is not a dict"
		#print "this transformed to string is "+str(a)
		return str(currentVal)
	elif type(currentVal) is types.DictType:
		#print "it is a dict"
		r = {}
		for key in currentVal:
			#print "this is a value with key "+key
			#print a[key]
			r[str(key)]=valsInString(currentVal[key])
		#print(r)
		return r
	elif type(currentVal) is types.ListType:
		r = []
		for thisSubList in currentVal:
			## print thisSubList
			r.append(valsInString(thisSubList))
		return r

data = valsInString(json.loads(open('all.json','r').read()))
fileR = open('symbolsstocks.json', 'w+')
symbols = {}
for key_i in data:
	depth = 1
	for industry in data[key_i]:
		depth = 2
		if(type(industry) is types.DictType):
			depth = 3
			industryName = industry.keys()[0]
			print "-"*depth*2+u"\u2713"+" "+industryName+" is a dictionary"
			if(type(industry[industryName]) is types.ListType):
				depth = 4
				print "-"*depth*2+u"\u2713"+" the values inside the dict are list"
				if len(industry[industryName])>=3:
					depth = 5
					print "-"*depth*2+u"\u2713"+" the length is bigger than 3"
					for hh in range(2, len(industry[industryName])):
						symbol_request = requests.get(\
							"http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+\
							industry[industryName][hh]\
							+"&callback=YAHOO.Finance.SymbolSuggest.ssCallback")
						if symbol_request.status_code == requests.codes.ok:
							depth = 6
							print "-"*depth*2+u"\u2713"+" the symbol request was successful"
							match = None
							try:
								match = re.search('symbol\":\"\w+\.?\w+\",', str(symbol_request.text.encode('ascii', 'strict')))
							except:
								print "-"*depth*2+u"\u2713"+" the match suffered from an error"
							if match != None:
								depth = 7
								symbol = match.group(0).replace('symbol":"','').replace('",','')
								print "-"*depth*2+u"\u2713"+" the symbol was found "+industry[industryName][hh]+"="+symbol
								symbols[industry[industryName][hh]] = symbol
							else:
								print "-"*depth*2+u"\u2717"+" the symbol was not found"
						else:
							print "-"*depth*2+u"\u2717"+" the symbol request was not successful"
				else:
					print "-"*depth*2+u"\u2717"+" there are less than 3 items"
			else:
				print "-"*depth*2+u"\u2717"+" the values are not a list"
				symbols[industryName] = industry[industryName]
		else:
			print "-"*depth*2+u"\u2717"+" the industry is not a dictionary"+str(type(industry))

print symbols
try:
	json.dump(symbols, fileR)
	fileR.close()
	print u"\u2717"*10+" Saving on file was successful"
except:
	print u"\u2717"+" Saving on file was not successful"