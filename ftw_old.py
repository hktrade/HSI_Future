from futu import *
import sys
import urllib
import urllib.request
from bs4 import BeautifulSoup
from futu.quote.quote_get_warrant import Request
import time
import csv
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
'''
https://futunnopen.github.io/futu-api-doc/api/Quote_API.html#get-warrant

rate 10000/1
street rate 5%-10%
recycle		3%-4%

法兴 法巴 摩通 

'''
k=0#		ftw.csv 	details of futu api
vol_v_a=[]
vol_a_a=[]
	
if str(sys.argv).find('-x')!=-1:
	req=Request()
	req.sort_field=SortField.TURNOVER
	req.status=WarrantStatus.NORMAL
	req.street_min=5
	req.street_max=50
	req.cur_price_min=0.060
	req.cur_price_max=0.120
	req.conversion_min = 10000
	req.conversion_max = 10000

	req.type_list=['BULL']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
	data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)
	# print(data[['stock','recovery_price','cur_price','turnover','change_rate','type','issuer']].iloc[-8:])
	
	# print(data[['issuer','conversion_ratio','street_rate','issue_size']].iloc[-8:])
	
	f=open(r'ftw.csv','w');f.write('');f.close()
	
	csvFile = open('ftw.csv','a+', newline='')
	write_ok = csv.writer(csvFile)	

	for i in data[['stock','recovery_price','cur_price','turnover','type','issuer']].iloc[-8:].values:
		write_ok.writerow(i)

	req.cur_price_min=0.040
	req.cur_price_max=0.100
	req.type_list=['BEAR']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)	
	data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size
	# print(data[['stock','recovery_price','cur_price','turnover','change_rate','type','issuer']].iloc[-8:])
	# print(data[['issuer','conversion_ratio','street_rate','issue_size']].iloc[-8:])

	for i in data[['stock','recovery_price','cur_price','turnover','type','issuer']].iloc[-8:].values:
		write_ok.writerow(i)
		
	# for i in data[['issuer','conversion_ratio','street_rate','issue_size']].iloc[-8:].values:
		# f.write('\n%s'%i);		
		
	csvFile.close()	
	quote_ctx.close()
	sys.exit()
# d_sort.append([data_op['strike_time'].iloc[-1],data_op['option_strike_price'].iloc[-1],data_op['option_open_interest'].iloc[-1]])



if str(sys.argv).find('-b')!=-1:
	req=Request()
	req.sort_field=SortField.TURNOVER
	req.status=WarrantStatus.NORMAL
	req.street_min=5
	req.street_max=50
	req.conversion_min = 10000
	req.conversion_max = 10000

	req.type_list=['BULL']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
	data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)
	
	print(data[['stock','recovery_price','cur_price','turnover','change_rate','type','issuer']].iloc[-8:])	
	print(data[['issuer','conversion_ratio','street_rate','issue_size']].iloc[-8:])

	req.type_list=['BEAR']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)	
	data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size
	print(data[['stock','recovery_price','cur_price','turnover','change_rate','type','issuer']].iloc[-8:])
	print(data[['issuer','conversion_ratio','street_rate','issue_size']].iloc[-8:])

	quote_ctx.close()
	sys.exit()
# d_sort.append([data_op['strike_time'].iloc[-1],data_op['option_strike_price'].iloc[-1],data_op['option_open_interest'].iloc[-1]])


if str(sys.argv).find('-t')!=-1:
	req=Request()
	req.sort_field=SortField.TURNOVER #STREET_RATE
	req.status=WarrantStatus.NORMAL
	req.street_min=5
	# req.cur_price_min=0.080
	# req.cur_price_max=0.120
	req.type_list=['BULL','BEAR']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.00700", req)
	
	data['turnover'] =data.apply(lambda x: int(x['turnover'] / 1000000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size
	if ret!=-1 and len(data)>0:
		print(data[['stock','recovery_price','cur_price','turnover','change_rate','type']].iloc[-16:])
		print(data[['issuer','conversion_ratio','street_rate','issue_size']].iloc[-16:])
###
	req.type_list=['CALL','PUT']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.00700", req)	
	if ret!=-1 and len(data)>0:
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 1000000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size
		print(data[['stock','strike_price','cur_price','turnover','change_rate','type']].iloc[-16:])
		print(data[['issuer','street_rate','issue_size']].iloc[-16:])
#https://openapi.futunn.com/futu-api-doc/en/quote/get-warrant.html#get-warrant-2
#http://www.aastocks.com/tc/stocks/quote/detail-quote.aspx?symbol=17377
#http://www.aastocks.com/tc/stocks/quote/detailchart.aspx?symbol=00700
	quote_ctx.close()
	sys.exit()
	

if str(sys.argv).find('-f')!=-1: # HSI options
	emp={'time':[],'strike_price':[],'open_interest':[],'option_type':[]};
	d_sort=[]
	
	data_sort=pd.DataFrame(emp)	
	ret, data = quote_ctx.get_option_chain('HK.800000',index_option_type=IndexOptionType.NORMAL)#,option_cond_type=OptionCondType.WITHIN)
	drop=[]

	for i in range(len(data)):
		if data['code'].iloc[i].find('0929C')!=-1: # 27
			drop.append(i)
	data=data.drop(drop,axis=0)

	for i in range(len(data)):		# print(data.iloc[i])
		if i%50==0:time.sleep(30)
		ret, data_op = quote_ctx.get_market_snapshot(data['code'].iloc[i])
		if len(data_op)>0 and data_op['option_open_interest'].iloc[-1]<1500:continue
		if len(data_op)>0:
			data_sort=data_sort.append({'time':data_op['strike_time'].iloc[-1],'strike_price':data_op['option_strike_price'].iloc[-1],'open_interest':data_op['option_open_interest'].iloc[-1],'option_type':data_op['option_type'].iloc[-1]},ignore_index=True)
		
	data_sort.sort_values(by='open_interest',ascending=False,inplace=True)#axis=0
	data_sort=data_sort.sort_values(by='open_interest',ascending=False)
		
	print(data_sort[['time','strike_price','open_interest','option_type']])
	
	# quote_ctx.close()
	# sys.exit()
####
	data_sort=pd.DataFrame(emp)	
	ret, data = quote_ctx.get_option_chain('HK.800000',index_option_type=IndexOptionType.NORMAL)#,option_cond_type=OptionCondType.WITHIN)
	drop=[]
	for i in range(len(data)):
		if data['code'].iloc[i].find('0929C')!=-1:
			drop.append(i)
	data=data.drop(drop,axis=0)
	
	for i in range(len(data)):		# print(data.iloc[i])
		if i%50==0:time.sleep(30)
		ret, data_op = quote_ctx.get_market_snapshot(data['code'].iloc[i])
		if len(data_op)>0 and data_op['option_open_interest'].iloc[-1]<2000:continue
		if len(data_op)>0:
			data_sort=data_sort.append({'time':data_op['strike_time'].iloc[-1],'strike_price':data_op['option_strike_price'].iloc[-1],'open_interest':data_op['option_open_interest'].iloc[-1],'option_type':data_op['option_type'].iloc[-1]},ignore_index=True)
		
	data_sort.sort_values(by='open_interest',ascending=False,inplace=True)#axis=0
	data_sort=data_sort.sort_values(by='open_interest',ascending=False)
		
	print(data_sort[['time','strike_price','open_interest','option_type']])
	
	quote_ctx.close()
	sys.exit()
	
	#700 lots>5000
	# US or HK options
	#,option_cond_type=OptionCondType.WITHIN)
	
if str(sys.argv).find('-s')!=-1: 

#option_implied_volatility
#option_delta

	emp={'time':[],'strike_price':[],'open_interest':[],'option_type':[],'code':[],'imp_vol':[],'delta':[]};
	data_sort=pd.DataFrame(emp)
	d_sort=[]
	code_US='US.AAPL'

	ret, data = quote_ctx.get_option_chain(code_US,index_option_type=IndexOptionType.NORMAL)
	print('\n',code_US,' len : ',len(data))
	print(data['code'])
		
	for i in range(len(data)):
		if i%50==0:
			time.sleep(30);		print(i)
		ret, data_op = quote_ctx.get_market_snapshot(data['code'].iloc[i])
		if ret==-1:continue
		if len(data_op)>0 and data_op['option_open_interest'].iloc[-1]<2999:continue
		if len(data_op)>0:
			data_sort=data_sort.append({'time':data_op['strike_time'].iloc[-1],'strike_price':data_op['option_strike_price'].iloc[-1],
			'open_interest':data_op['option_open_interest'].iloc[-1],'option_type':data_op['option_type'].iloc[-1],
			'code':data_op['code'].iloc[-1],'imp_vol':data_op['option_implied_volatility'].iloc[-1],'delta':data_op['option_delta'].iloc[-1]},ignore_index=True)
		
	data_sort.sort_values(by='open_interest',ascending=False,inplace=True)#axis=0
	data_sort=data_sort.sort_values(by='open_interest',ascending=False)
		
	print(data_sort[['time','strike_price','open_interest','option_type']])	
	print(data_sort[['time','code','imp_vol','delta']])	
	quote_ctx.close()
	sys.exit()
	
	
# lot_size 100

	# drop=[]
	# for i in range(len(data)):
		# if data['code'].iloc[i].find('C')!=-1:
			# drop.append(i)
	# data=data.drop(drop,axis=0)
	
	# print(data.iloc[i])
	

	# print(data[['option_strike_price','option_contract_size']])	
	# for i in data.keys().tolist():
		# print(i)
	# print(data.keys())
	
#https://futunnopen.github.io/futu-api-doc/api/Base_API.html#tickertype
# 20 times in 1 minute
# c = a if a>b else b