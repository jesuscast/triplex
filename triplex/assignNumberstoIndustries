import requests
import json
sectors = {'Financial': ['Accident & Health Insurance', 'Asset Management', 'Closed-End Fund - Debt', 'Closed-End Fund - Equity', 'Closed-End Fund - Foreign', 'Credit Services', 'Diversified Investments', 'Foreign Money Center Banks', 'Foreign Regional Banks', 'Insurance Brokers', 'Investment Brokerage - National', 'Investment Brokerage - Regional', 'Life Insurance', 'Money Center Banks', 'Mortgage Investment', 'Property & Casualty Insurance', 'Property Management', 'Real Estate Development', 'Regional - Mid-Atlantic Banks', 'Regional - Midwest Banks', 'Regional - Northeast Banks', 'Regional - Pacific Banks', 'Regional - Southeast Banks', 'Regional - Southwest  Banks', 'REIT - Diversified', 'REIT - Healthcare Facilities', 'REIT - Hotel/Motel', 'REIT - Industrial', 'REIT - Office', 'REIT - Residential', 'REIT - Retail', 'Savings & Loans', 'Surety & Title Insurance'], 'Conglomerates': ['Conglomerates'], 'Healthcare': ['Biotechnology', 'Diagnostic Substances', 'Drug Delivery', 'Drug Manufacturers - Major', 'Drug Manufacturers - Other', 'Drug Related Products', 'Drugs - Generic', 'Health Care Plans', 'Home Health Care', 'Hospitals', 'Long-Term Care Facilities', 'Medical Appliances & Equipment', 'Medical Instruments & Supplies', 'Medical Laboratories & Research', 'Medical Practitioners', 'Specialized Health Services'], 'Utilities': ['Diversified Utilities', 'Electric Utilities', 'Foreign Utilities', 'Gas Utilities', 'Water Utilities'], 'Consumer Goods': ['Appliances', 'Auto Manufacturers - Major', 'Auto Parts', 'Beverages - Brewers', 'Beverages - Soft Drinks', 'Beverages - Wineries & Distillers', 'Business Equipment', 'Cigarettes', 'Cleaning Products', 'Confectioners', 'Dairy Products', 'Electronic Equipment', 'Farm Products', 'Food - Major Diversified', 'Home Furnishings & Fixtures', 'Housewares & Accessories', 'Meat Products', 'Office Supplies', 'Packaging & Containers', 'Paper & Paper Products', 'Personal Products', 'Photographic Equipment & Supplies', 'Processed & Packaged Goods', 'Recreational Goods', 'Recreational Vehicles', 'Rubber & Plastics', 'Sporting Goods', 'Textile - Apparel Clothing', 'Textile - Apparel Footwear & Accessories', 'Tobacco Products', 'Toys & Games', 'Trucks & Other Vehicles'], 'Industrial Goods': ['Aerospace/Defense - Major Diversified', 'Aerospace/Defense Products & Services', 'Cement', 'Diversified Machinery', 'Farm & Construction Machinery', 'General Building Materials', 'General Contractors', 'Heavy Construction', 'Industrial Electrical Equipment', 'Industrial Equipment & Components', 'Lumber', 'Machine Tools & Accessories', 'Manufactured Housing', 'Metal Fabrication', 'Pollution & Treatment Controls', 'Residential Construction', 'Small Tools & Accessories', 'Textile Industrial', 'Waste Management'], 'Services': ['Advertising Agencies', 'Air Delivery & Freight Services', 'Air Services', 'Apparel Stores', 'Auto Dealerships', 'Auto Parts Stores', 'Auto Parts Wholesale', 'Basic Materials Wholesale', 'Broadcasting - Radio', 'Broadcasting - TV', 'Building Materials Wholesale', 'Business Services', 'Catalog & Mail Order Houses', 'CATV Systems', 'Computers Wholesale', 'Consumer Services', 'Department Stores', 'Discount', 'Drug Stores', 'Drugs Wholesale', 'Education & Training Services', 'Electronics Stores', 'Electronics Wholesale', 'Entertainment - Diversified', 'Food Wholesale', 'Gaming Activities', 'General Entertainment', 'Grocery Stores', 'Home Furnishing Stores', 'Home Improvement Stores', 'Industrial Equipment Wholesale', 'Jewelry Stores', 'Lodging', 'Major Airlines', 'Management Services', 'Marketing Services', 'Medical Equipment Wholesale', 'Movie Production', 'Music & Video Stores', 'Personal Services', 'Publishing - Books', 'Publishing - Newspapers', 'Publishing - Periodicals', 'Railroads', 'Regional Airlines', 'Rental & Leasing Services', 'Research Services', 'Resorts & Casinos', 'Restaurants', 'Security & Protection Services', 'Shipping', 'Specialty Eateries', 'Specialty Retail', 'Sporting Activities', 'Sporting Goods Stores', 'Staffing & Outsourcing Services', 'Technical Services', 'Toy & Hobby Stores', 'Trucking', 'Wholesale'], 'Basic Materials': ['Agricultural Chemicals', 'Aluminum', 'Chemicals - Major Diversified', 'Copper', 'Gold', 'Independent Oil & Gas', 'Industrial Metals & Minerals', 'Major Integrated Oil & Gas', 'Nonmetallic Mineral Mining', 'Oil & Gas Drilling & Exploration', 'Oil & Gas Equipment & Services', 'Oil & Gas Pipelines', 'Oil & Gas Refining & Marketing', 'Silver', 'Specialty Chemicals', 'Steel & Iron', 'Synthetics'], 'Technology': ['Application Software', 'Business Software & Services', 'Communication Equipment', 'Computer Based Systems', 'Computer Peripherals', 'Data Storage Devices', 'Diversified Communication Services', 'Diversified Computer Systems', 'Diversified Electronics', 'Healthcare Information Services', 'Internet Information Providers', 'Internet Service Providers', 'Internet Software & Services', 'Long Distance Carriers', 'Multimedia & Graphics Software', 'Networking & Communication Devices', 'Personal Computers', 'Printed Circuit Boards', 'Processing Systems & Products', 'Scientific & Technical Instruments', 'Security Software & Services', 'Semiconductor - Broad Line', 'Semiconductor - Integrated Circuits', 'Semiconductor - Specialized', 'Semiconductor Equipment & Materials', 'Semiconductor- Memory Chips', 'Technical & System Software', 'Telecom Services - Domestic', 'Telecom Services - Foreign', 'Wireless Communications', 'Information & Delivery Services', 'Information Technology Services']}
newSectors = {}
fileRR = open('result.json','w+')
for key in sectors:
	print "Sector "+key
	newSectors[key] = []
	for industry in sectors[key]:
		#print "---"+industry+":"
		validNumber = False
		number = 0
		while(validNumber == False):
			try:
				number = input("---"+industry+":")
				if isinstance(number, int):
					validNumber = True
			except:
		 		print("invalid entrance")
		newFileName = str(number)+"conameu.csv"
		#response = urllib2.urlopen('http://biz.yahoo.com/p/csv/'+newFileName)
		r = requests.get('http://biz.yahoo.com/p/csv/'+newFileName)
		if r.status_code == requests.codes.ok:
			print "---"+u"\u2713"+" File Downloaded"
			stocks = []
			listRawTemp = r.text.split("\n")
			for indexT in range(1, len(listRawTemp)-1):
				try:
					print "------"+u"\u2713"+" Stock Added"
					namme=str(listRawTemp[indexT].split(",")[0]).replace('"','')
					stocks.append(namme)
				except:
					print "------"+u"\u2717"+" Stock Added Failed to add"
			newSectors[key].append({industry:stocks})
		else:
			print "---"+u"\u2717"+" File Failed to Download"
			newSectors[key].append({industry:number})
#json.dump(newSectors, fileRR)