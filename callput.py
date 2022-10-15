from futu import *
import sys
from futu.quote.quote_get_warrant import Request
import time
import csv
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)#42.193.124.183

k=0#		details of futu api
vol_v_a=[]
vol_a_a=[]

def snap_one(symbol):
	ret, data = quote_ctx.get_market_snapshot(symbol)
	if ret != RET_OK:
		def_str('error, get_market_snapshot ')
		print(data)
		return(0)
	else:
		return(data['last_price'][0])

def snap_list(op_list): # 传入代码列表 获取快照 最大 400只
	data=pd.DataFrame({'bid_price':[],'ask_price':[]})
	ret=-1;	ret_i = 0
	op_list = op_list[0:400]
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
	# data = data.rename(columns = {" ":" "})
	return(data[['code','turnover','stock_owner','last_price','bid_price','ask_price','wrt_type','wrt_delta']])

def get_callput(symbol):
	req=Request()
	req.sort_field=SortField.TURNOVER
	req.status=WarrantStatus.NORMAL
###
	req.type_list=['CALL']
	# req.type_list=['PUT']
	
	ret , (data, last_page, all_count) = quote_ctx.get_warrant(symbol, req)
	
	if ret!=-1 and len(data)>0:
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size

		data = data.rename(columns = {"recovery_price":"recovery"})
		data = data.rename(columns = {"street_rate":"street"})
		
		#price_change_val
		data_P = data.rename(columns = {"implied_volatility":"iv"}) #引伸波幅 

		# print(data_P[['stock','cur_price','turnover','type','street','change_rate','strike_price','iv','delta']].tail(5))

# 敏感度算法：正股每单位价格*对冲值/（换股比率*窝轮每单位价格）
# stock price * delta / 10000 * callput price

	if len(data_P)>0:
		data_P = snap_list(list(data_P['stock']))
		data_P['spread'] = data_P['ask_price'] - data_P['bid_price'] == 0.01
		# data_P = data_P[data_P['bid_price'] > 0]
		data_P = data_P[data_P['turnover'] > 1]
		# data_P = data_P[data_P['spread'] == True]#只取买卖价差为0.01的轮
		
	print(len(data_P))
	return(data_P)

df = get_callput('HK.00700')
print(df)
# print(df[df['wrt_type']=='PUT'])

quote_ctx.close()
sys.exit()