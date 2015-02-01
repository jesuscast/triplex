import subprocess
import json

json_sectors = open("industries_and_sectors.json",'r')
sectors = json.loads(json_sectors.read())
json_sectors.close()

json_symbols = open("stock_symbols.json","r")
symbols = json.loads(json_symbols.read())
json_symbols.close()

wrong = u"\u2717" #unicode symbol for X mark for wrong answers
right = u"\u2713" #unicode symbol for check mark for right answers

rightN = 0
wrongN = 0

missing_stocks = []
missing_sectors = []

for key_i in sectors:
	for sector_dict in sectors[key_i]:
		sector_list = sector_dict[sector_dict.keys()[0]]
		if isinstance(sector_list, list):
			i = 0
			for stock_name in sector_list:
				if(i>1):
					if symbols.has_key(stock_name):
						print(right),
						continue
					else:
						print(wrong),
						missing_stocks.append(stock_name)
				else:
					i += 1
					continue
		else:
			print(wrong),
			missing_sectors.append([sector_dict.keys()[0], sector_list])
			continue

subprocess.call("touch missing_stocks.json", shell=True)
file_stocks = open("missing_stocks.json",'w')
json.dump(missing_stocks, file_stocks)
file_stocks.close()

subprocess.call("touch missing_sectors.json", shell=True)
file_sectors = open("missing_sectors.json",'w')
json.dump(missing_sectors, file_sectors)
file_sectors.close()