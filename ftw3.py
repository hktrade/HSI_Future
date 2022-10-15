from futu import *
import sys
from futu.quote.quote_get_warrant import Request
import time
import csv
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)#42.193.124.183

k=0#		ftw.csv 	details of futu api
vol_v_a=[]
vol_a_a=[]

def snap_list(op_list): # 传入代码列表 获取快照 最大 400只
	data=pd.DataFrame({'bid_price':[],'ask_price':[]})
	ret=-1;	ret_i = 0
	op_list = op_list[0:400]
	# print(op_list)
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
	return(data[['code','turnover','stock_owner','last_price','bid_price','ask_price']])
	
if str(sys.argv).find('-b')!=-1 or str(sys.argv).find('-b')==-1:
	req=Request()
	req.sort_field=SortField.TURNOVER # sort by turnover
	req.status=WarrantStatus.NORMAL
	req.street_min=0.1 # street rate
	req.street_max=99.9 
	# req.cur_price_min=0.010 # min max price
	# req.cur_price_max=0.300 

	# req.issuer_list = ['BI','HT','HS','CS','UB','BP','SG','VT'] # less BI HS UB 
	req.conversion_min = 10000
	req.conversion_max = 10000

	f=open(r'ftw.csv','w');f.write('');f.close()	
	csvFile = open('ftw.csv','a+', newline='')
	write_ok = csv.writer(csvFile)
###
	req.type_list=['CALL']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
	
	if ret!=-1 and len(data)>0:# lambda x:'%.2f' % x
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)

		data = data.rename(columns = {"recovery_price":"recovery"})
		data = data.rename(columns = {"street_rate":"street"})
		data_C = data.rename(columns = {"price_change_val":"change"})
		print(data_C[['stock','cur_price','turnover','type','street','change','strike_price']].tail(5))
	
	req=Request()
	req.sort_field=SortField.TURNOVER
	req.status=WarrantStatus.NORMAL
	req.street_min=0.1
	req.street_max=99.9

	req.type_list=['PUT']
	
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
	
	if ret!=-1 and len(data)>0:
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size

		data = data.rename(columns = {"recovery_price":"recovery"})
		data = data.rename(columns = {"street_rate":"street"})
		data_P = data.rename(columns = {"price_change_val":"change"})
		print(data_P[['stock','cur_price','turnover','type','street','change','strike_price']].tail(5))
	
	print('\n\n\n\n')
	print(len(data_C),len(data_P))
	data_C = snap_list(list(data_C['stock']))
	data_C['spread'] = data_C['ask_price'] - data_C['bid_price'] == 0.01
	data_C = data_C[data_C['bid_price'] > 1]
	data_C = data_C[data_C['spread'] == True]
	
	data_P = snap_list(list(data_P['stock']))
	data_P['spread'] = data_P['ask_price'] - data_P['bid_price'] == 0.01
	data_P = data_P[data_P['bid_price'] > 1]
	data_P = data_P[data_P['spread'] == True]
	
# 得到的数据 筛选后是否是空的
	print(data_C)
	print(data_P)
	
	csvFile.close()	
	quote_ctx.close()
	sys.exit()