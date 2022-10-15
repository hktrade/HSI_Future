import requests,logging,time
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import csv,os,os.path
import alpaca_trade_api as tradeapi
import urllib.request,requests
from urllib import error, parse
from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
# https://openapi.futunn.com/futu-api-doc/quote/get-future-info.html
def snap_op(symbol):
	data=pd.DataFrame({'bid_price':[],'ask_price':[]})
	ret=-1;	ret_i=0; 
	while ret==-1:
		ret_i += 1
		if ret_i > 3:
			print(' snap_op error >3 ')
			break
		ret, data = quote_ctx.get_market_snapshot(symbol)
		if ret==-1:
			print('snap_op -1 '+str(data))
			data=pd.DataFrame({'bid_price':[],'ask_price':[]});		time.sleep(3);
		else:
			break
		time.sleep(2)
	return(data[['code','option_delta','option_open_interest','turnover','stock_owner','option_strike_price','strike_time','last_price','bid_price','ask_price']])
	
def snap_list(op_list):
	data=pd.DataFrame({'bid_price':[],'ask_price':[]})
	ret=-1;	ret_i = 0
	while ret==-1:
		ret_i += 1
		if ret_i > 3:
			print(' snap_list error >3 ')
			break
		ret, data = quote_ctx.get_market_snapshot(op_list)
		if ret==-1:
			print('snap_list -1 '+str(data));		time.sleep(3);
		else:
			break
		time.sleep(2)
	return(data[['code','option_delta','option_open_interest','turnover','stock_owner','option_strike_price','strike_time','last_price','bid_price','ask_price']])
	
def get_hkop(*any):
	print(len(any))
	if len(any)>1:
		symbol = any[0]
	else:
		symbol = any[0]
	print(symbol)
	emp={'time':[],'strike_price':[],'open_interest':[],'option_type':[]};
	data_sort=pd.DataFrame(emp)	
	ret, df = quote_ctx.get_option_chain(symbol)
	if ret==-1:
		print(df)
	if len(any)==3:
		max = float(any[2]); min = float(any[1])
		print(min, max, type(max))
		df = df[df['strike_price'] < max] # arg includes min and max
		df = df[df['strike_price'] > min]
	return(df)
# Index(['code', 'name', 'lot_size', 'stock_type', 'option_type', 'stock_owner',
       # 'strike_time', 'strike_price', 'suspension', 'stock_id',
       # 'index_option_type'],
# df = get_hkop('HK.00700', 300, 350)
# print(df[['code','stock_owner', 'strike_price']])

df = get_hkop('HK.00700')
print(df[['code','stock_owner', 'strike_price']])

# quote_ctx.close() #假设同时监控10只港股，期权的价格在某范围之内， 买卖价差在设置的范围之内
# sys.exit()        #每 30 秒内最多请求 60 次（400）快照。

dfop = snap_list(list(df['code'])[0:400]) # output stock symbol :
dfop = dfop[dfop['bid_price'] > 1]
dfop['spread'] = dfop['ask_price'] - dfop['bid_price'] == 0.01 # setting
df_true = dfop[dfop['spread'] == True]
print(df_true[['code','ask_price','bid_price']])
quote_ctx.close()
sys.exit()