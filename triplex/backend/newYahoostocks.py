__author__ = 'jesusandrescastanedasosa'

import requests
from datetime import date
import time
import re
import json
def sectorData(sector='^YHOh722', from_date={'month':1, 'day': 1, 'year':2014}, to_date={'month':-1}):
    request_info = {}
    request_info['base_url']='http://finance.yahoo.com/'+\
                            '_td_charts_api/resource/charts;'+\
                            'comparisonTickers=;'+\
                            'events=div|split|earn;'\
                            'gmtz=-5;'+\
                            'indicators=quote;'+\
                            'period1=1417928400;'+\
                            'period2=1419726847;'+\
                            'queryString='+\
                            '{"s":"%5EYHOh722"};'+\
                            'range=5d;'+\
                            'rangeSelected=undefined;'+\
                            'ticker=^YHOH722;'+\
                            'useMock=false'
    request_info['params'] = {}
    request_info['params']['crumb'] = 'kjNcnhBPdI.'
    #cookies = dict(B='45ao6bpa75a7h&b=3&s=of', ywandp='1000911397279%3A2262158347', fpc='1000911397279%3AZSx3ojh9%7C%7C', ywadp115488662='348323426', ypcdb='7ffa505ef392c14f9624126a9bc1eaed', V='v=0.7&m=1&ccOptions=%7B%22show%22%3Afalse%2C%22lang%22%3A%22en%22%2C%22fontSize%22%3A24%2C%22fontName%22%3A%22Helvetica%20Neue%2CHelvetica%2CArial%2C_sans%22%2C%22fontColor%22%3A%22%23ffffff%22%2C%22fontOpacity%22%3A1%2C%22fontEffect%22%3A%22none%22%2C%22bgColor%22%3A%22%23000000%22%2C%22bgOpacity%22%3A0.75%7D', yvap='193@yvap=193@cc=2@al=0@vl=10@rvl=7@ac=1@rvl_NFL=0@session_NFL=0@lmsID=@rcc=0', PRF='=undefined&t=^YHOH722+AAPL+YHOO')

    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',\
    'Accept-Encoding':'gzip, deflate, sdch',\
    'Accept-Language':'en-US,en;q=0.8,es;q=0.6,fr;q=0.4',\
    'Cache-Control':'max-age=0',\
    'Connection':'keep-alive',\
    'Cookie':'B=45ao6bpa75a7h&b=3&s=of; ywandp=1000911397279%3A2262158347; fpc=1000911397279%3AZSx3ojh9%7C%7C; ywadp115488662=348323426; ypcdb=7ffa505ef392c14f9624126a9bc1eaed; V=v=0.7&m=1&ccOptions=%7B%22show%22%3Afalse%2C%22lang%22%3A%22en%22%2C%22fontSize%22%3A24%2C%22fontName%22%3A%22Helvetica%20Neue%2CHelvetica%2CArial%2C_sans%22%2C%22fontColor%22%3A%22%23ffffff%22%2C%22fontOpacity%22%3A1%2C%22fontEffect%22%3A%22none%22%2C%22bgColor%22%3A%22%23000000%22%2C%22bgOpacity%22%3A0.75%7D; yvap=193@yvap=193@cc=2@al=0@vl=10@rvl=7@ac=1@rvl_NFL=0@session_NFL=0@lmsID=@rcc=0; PRF==undefined&t=^YHOH722+AAPL+YHOO',\
    'Host':'finance.yahoo.com',\
    'If-None-Match':'W/"zbJ6kQkWdLm3/jCaI8Ierw=="',\
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',\
    }
    stocks_request = requests.get(request_info['base_url'], params=request_info['params'], headers=headers)
    if stocks_request.status_code == requests.codes.ok:

        return json.loads(stocks_request.text)
    else:
        return False

def current(stocks = ['GOOG','YHOO']):
    request_info = {}
    request_info['base_url']='http://download.finance.yahoo.com/d/quotes.csv'
    request_info['stocks'] = stocks
    request_info['properties'] = ['n','s','l1','o','p']
    request_info['format'] = '.csv'
    request_info['params'] = {}
    request_info['params']['s'] = ','.join(request_info['stocks'])
    request_info['params']['e'] = request_info['format']
    request_info['params']['f'] = ''.join(request_info['properties'])
    stocks_information = requests.get(request_info['base_url'], params=request_info['params'])
    if stocks_information.status_code == requests.codes.ok:
        result = [[item.replace('\"','') for item in this_stock.split(',')] for this_stock in stocks_information.text.split('\r\n')]
        result.pop(len(result)-1)
        return result
    else:
        return False


def historical(stock='GOOG', from_date={'month':1, 'day': 1, 'year':2014}, to_date={'month':-1}):
    if to_date['month'] == -1:
        current_date = date.today().timetuple()[:3]
        to_date['month'] = current_date[1]
        to_date['day'] = current_date[2]
        to_date['year'] = current_date[0]
    request_info = {}
    request_info['base_url'] = 'http://ichart.yahoo.com/table.csv'
    request_info['stocks'] = stock
    request_info['format'] = '.csv'
    request_info['params'] = {}
    request_info['params']['s'] = stock
    request_info['params']['a'] = from_date['month']-1
    #minus one because that's how the API works
    request_info['params']['b'] = from_date['day']
    request_info['params']['c'] = from_date['year']
    request_info['params']['d'] = to_date['month']-1
    #minus one because that's how the API works
    request_info['params']['e'] = to_date['day']
    request_info['params']['f'] = to_date['year']
    intervals = {'daily': 'd', 'monthly': 'm', 'weekly': 'w'}
    request_info['params']['g'] = intervals['daily']
    request_info['params']['ignore'] = request_info['format']
    final_url = request_info['base_url'] + '?s='\
                +request_info['params']['s']\
                + "&a=" + str(request_info['params']['a'])\
                + "&b=" + str(request_info['params']['b'])\
                + "&c=" + str(request_info['params']['c'])\
                + "&d=" + str(request_info['params']['d'])\
                + "&e=" + str(request_info['params']['e'])\
                + "&f=" + str(request_info['params']['f'])\
                + "&g=" + request_info['params']['g']\
                + "&ignore=" + request_info['params']['ignore']
    stocks_information = requests.get(final_url)
    if stocks_information.status_code == requests.codes.ok:
        result = [[item.replace('\"','') for item in this_stock.split(',')] for this_stock in stocks_information.text.split('\n')]
        result.pop(0)
        result.pop(len(result)-1)
        # ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
        return result
    else:
        return False


def realtime(stock='GOOG', range='1d'):
    request_info = {}
    request_info['format'] = "csv"
    request_info['base_url'] = "http://chartapi.finance.yahoo.com/instrument/1.1/"+\
                               stock+"/chartdata;type=quote;range="+\
                               range+"/"+request_info['format']
    data = requests.get(request_info['base_url'])
    if data.status_code == requests.codes.ok:
        #17 starting from 17 we have the data, before that is info of the company
        data_list = data.text.split('\n')[17:]
        data_list_table = [[re.sub('[^0-9.]', '', k) for k in n.split(',')] for n in data_list]
        data_list_table.pop(len(data_list_table)-1)
        return data_list_table
    else:
        return False