__author__ = 'jesusandrescastanedasosa'

import requests
from datetime import date
import time
import re

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
        #print final_url
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
    print request_info['base_url']
    if data.status_code == requests.codes.ok:
        #17 starting from 17 we have the data, before that is info of the company
        data_list = data.text.split('\n')[17:]
        data_list_table = [[re.sub('[^0-9.]', '', k) for k in n.split(',')] for n in data_list]
        data_list_table.pop(len(data_list_table)-1)
        return data_list_table
    else:
        return False