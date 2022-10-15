from futu import *
import sys
import urllib
import urllib.request
import time
import csv
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# df[df['code'].str.contains('.BK')]['qty'] = 0
	
def snap_list(op_list): # symbol list, get snapshot
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
	return(data[['code','option_open_interest','turnover','option_strike_price','last_price']])
	
def get_interest(symbol): #get_option_chain
	emp={'time':[],'strike_price':[],'option_open_interest':[],'option_type':[]};
	d_sort=[];drop=[]
	
	data_sort=pd.DataFrame(emp)	
	ret, data = quote_ctx.get_option_chain(symbol,index_option_type=IndexOptionType.NORMAL)#,option_cond_type=OptionCondType.WITHIN)
	# print(data['option_type'],type(data['strike_time'].iloc[0]))
	# print(len(data),data.keys())
	
	# data_C = data[data['code'].str.contains('0929C')]
	# data_P = data[data['code'].str.contains('0929P')]
	data = data[data['strike_time'] > '2022-09-03'] # search date > 09 03
	# data = data[data['strike_time'] < '2022-09-24']
	data_C = data[data['option_type']=='CALL']
	data_P = data[data['option_type']=='PUT']
	
	# quote_ctx.close()
	# sys.exit()
	print(data_P.keys())
	print(len(data_C),len(data_P))
	print(data_C['strike_time'])

	df_C = snap_list(list(data_C['code'])[0:400]) # snapshot max is 400
	df_C.sort_values(by='option_open_interest',ascending=False,inplace=True)
	df_C=df_C.sort_values(by='option_open_interest',ascending=False)
	
	df_P = snap_list(list(data_P['code'])[0:400])
	df_P.sort_values(by='option_open_interest',ascending=False,inplace=True)
	df_P=df_P.sort_values(by='option_open_interest',ascending=False)
	
	df_C = df_C.rename(columns = {"option_open_interest":"open"})
	df_P = df_P.rename(columns = {"option_open_interest":"open"})
	df_C = df_C.rename(columns = {"option_strike_price":"strike"})
	df_P = df_P.rename(columns = {"option_strike_price":"strike"})
	return(df_C,df_P)
# df_C = df_C.drop(df_C[df_C['option_open_interest']<1000].index)
# df_C = df_C[df_C['last_price'] < 8]
# df_C = df_C[df_C['last_price'] > 3]

df_C , df_P = get_interest('HK.800000')
df_C = df_C.drop(df_C[df_C['turnover']==0].index)
df_P = df_P.drop(df_P[df_P['turnover']==0].index)
print(df_C.head(5),df_P.head(5))
quote_ctx.close()
sys.exit()

