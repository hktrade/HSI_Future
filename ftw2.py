from futu import *
import sys
from futu.quote.quote_get_warrant import Request
import time
import csv
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)#42.193.124.183

k=0#		ftw.csv 	details of futu api
vol_v_a=[]
vol_a_a=[]

if str(sys.argv).find('-b')!=-1 or str(sys.argv).find('-b')==-1:
	req=Request()
	req.sort_field=SortField.TURNOVER
	req.ascend = False
	req.status=WarrantStatus.NORMAL
	req.street_min=0.1
	req.street_max=99.9

	# req.issuer_list = ['BI','HT','HS','CS','UB','BP','SG','VT'] # less BI HS UB 
	req.conversion_min = 10000
	req.conversion_max = 10000

	f=open(r'ftw.csv','w');f.write('');f.close()	
	csvFile = open('ftw.csv','a+', newline='')
	write_ok = csv.writer(csvFile)
###
	req.type_list=['BULL']
	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req)
	
	if ret!=-1 and len(data)>0:# lambda x:'%.2f' % x
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)

		data.sort_values(by=['turnover'],ascending=True,inplace=True)
		data = data.rename(columns = {"recovery_price":"recovery"})
		data = data.rename(columns = {"street_rate":"street"})
		data = data.rename(columns = {"price_change_val":"change"})
		print(data[['stock','recovery','cur_price','turnover','type','street','change','issuer']].tail(20))
	
	# quote_ctx.close()
	# sys.exit()
	
	req2=Request()
	req2.sort_field=SortField.TURNOVER
	req2.ascend = False
	req2.type_list=['BEAR']

	req2.conversion_min = 10000
	req2.conversion_max = 10000

	ret , (data, last_page, all_count) = quote_ctx.get_warrant("HK.800000", req2)
	# print(ret,data[data['turnover'] > 0][['stock','recovery','cur_price','turnover','type','street','change','issuer']])
	
	if ret!=-1 and len(data)>0:
		data['turnover'] =data.apply(lambda x: int(x['turnover'] / 10000), axis=1)#issuer #conversion_ratio #name #street_rate #issue_size

		data.sort_values(by=['turnover'],ascending=True,inplace=True)
		data = data.rename(columns = {"recovery_price":"recovery"})
		data = data.rename(columns = {"street_rate":"street"})
		data = data.rename(columns = {"price_change_val":"change"})
		print(data[['stock','recovery','cur_price','turnover','type','street','change','issuer']].tail(5))
	
	csvFile.close()	
	quote_ctx.close()
	sys.exit()