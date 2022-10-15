# powered by hktrade.github.io
import json,sys,csv,time,re,os
import pandas as pd
from datetime import datetime,timedelta
from futu import *
import pandas_ta as ta#technical analysis

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
try:
	trd_ctx = OpenFutureTradeContext(host='127.0.0.1', port=11111,
	is_encrypt = False, security_firm=SecurityFirm.FUTUSECURITIES)
except:
	trd_ctx = OpenFutureTradeContext(host='127.0.0.1', port=11111)
	
def get_k(symbol, N): # 獲取分鐘K 支持 1 3 5 15 30 60 等
	def codes(i):
		switcher={1:SubType.K_1M,3:SubType.K_3M,5:SubType.K_5M,15:SubType.K_15M}
		return (switcher.get(i,"Invalid Symbols"))
	def codes2(i):
		switcher={1:KLType.K_1M,3:KLType.K_3M,5:KLType.K_5M,15:KLType.K_15M}
		return (switcher.get(i,"Invalid Symbols"))

	K_S = codes(N)
	K_type = codes2(N)

	ret_sub, err_message = quote_ctx.subscribe(symbol, [K_S], subscribe_push=False)
	if ret_sub!=0:
		print(ret_sub,err_message)
	
	ret, data3 = quote_ctx.get_cur_kline(symbol, 1000, K_type) # 最大支持 1000 跟 K
	if ret==-1 or len(data3)<2:
		print(symbol + '  kline error ')
		return None
	data3['time_key'] = pd.to_datetime(data3['time_key'])
	data3.set_index('time_key', inplace=True,drop=False)
	return(data3[['time_key','open','high','low','close','volume']])

def get_book(symbol):# 先訂閱買賣擺盤類型。訂閱成功後 OpenD 將持續收到服務器的推送，False 代表暫時不需要推送給腳本
	ret_sub = quote_ctx.subscribe([symbol], [SubType.ORDER_BOOK], subscribe_push=False)[0]
	if ret_sub == RET_OK:
		ret, data = quote_ctx.get_order_book(symbol, num=10) # ask bid 10 for every stock or future 
		if ret == RET_OK:
			return(data)
		else:
			return None
	else:
		print('subscription failed')#dict_keys(['code', 'svr_recv_time_bid', 'svr_recv_time_ask', 'Bid', 'Ask'])
		return None
F_bid = 0
F_vol = 0
class TickerTest(TickerHandlerBase):# 获取期指的Ticker 实时推送
	def on_recv_rsp(self, rsp_str):
		global F_bid,F_lst
		ret_code, data = super(TickerTest,self).on_recv_rsp(rsp_str)
		if ret_code != RET_OK:
			print("TickerTest: error, msg: %s" % data)
			return RET_ERROR, data
		print(data[['price','volume','turnover','ticker_direction','type']].tail(3),len(data))
		F_lst=data['price'].tail(3)
		F_bid=int(data['price'].iloc[-1])
		F_vol=int(data['volume'].iloc[-1])
		return RET_OK, data
def macd(data,short=0,long1=0,mid=0):
    if short==0:short=12
    if long1==0:long1=26
    if mid==0:mid=9
    data['sema']=pd.Series(data['close']).ewm(span=short,min_periods = 11).mean()
    data['lema']=pd.Series(data['close']).ewm(span=long1,min_periods = 11).mean()
    data.fillna(0,inplace=True)
    data['DIF']=data['sema']-data['lema']
    data['DEA']=pd.Series(data['DIF']).ewm(span=mid, min_periods = 8).mean()
    data['MACD']=2*(data['DIF']-data['DEA'])
    data.fillna(0,inplace=True)
    return data
while True:
	time.sleep(3) 
	symbol = 'HK.999010' #'HK.HSI2210'
	data = get_book(symbol)
	print(data.keys())
	df = pd.DataFrame(data)[['Ask','Bid']]
	print(df)
	print(df['Ask'][0][0], df['Ask'][0][1]) # ask 1 price and size
	print(df['Bid'][0][0], df['Bid'][0][1]) # bid 1 price and size 
		
	df = get_k(symbol,5) # get 5min K line , real time 
	df['vwap'] = df.ta.vwap() # get vwap 
	df = macd(df) #get macd 
	print(df[['close','volume','vwap','MACD']].tail(5))
	
	handler = TickerTest();quote_ctx.set_handler(handler);quote_ctx.subscribe(['HK.HSImain'], [SubType.TICKER])
	print(F_bid,F_vol)
	
quote_ctx.close()
trd_ctx.close()
sys.exit() # hktrade.github.io

# adx  atr  bbands  cci   cross    ema   hlc3     rsi   slope   sma   squeeze
# squeeze_pro  stoch KD  supertrend   ttm_trend  vwap  willr  
''' more than 100 indicators 
    aberration, above, above_value, accbands, ad, adosc, adx, alma, amat, ao, ao
bv, apo, aroon, atr, bbands, below, below_value, bias, bop, brar, cci, cdl_patte
rn, cdl_z, cfo, cg, chop, cksp, cmf, cmo, coppock, cross, cross_value, cti, deca
y, decreasing, dema, dm, donchian, dpo, ebsw, efi, ema, entropy, eom, er, eri, f
isher, fwma, ha, hilo, hl2, hlc3, hma, hwc, hwma, ichimoku, increasing, inertia,
 jma, kama, kc, kdj, kst, kurtosis, kvo, linreg, log_return, long_run, macd, mad
, massi, mcgd, median, mfi, midpoint, midprice, mom, natr, nvi, obv, ohlc4, pdis
t, percent_return, pgo, ppo, psar, psl, pvi, pvo, pvol, pvr, pvt, pwma, qqe, qst
ick, quantile, rma, roc, rsi, rsx, rvgi, rvi, short_run, sinwma, skew, slope, sm
a, smi, squeeze, squeeze_pro, ssf, stc, stdev, stoch, stochrsi, supertrend, swma
, t3, td_seq, tema, thermo, tos_stdevall, trima, trix, true_range, tsi, tsignals
, ttm_trend, ui, uo, variance, vhf, vidya, vortex, vp, vwap, vwma, wcp, willr, w
ma, xsignals, zlma, zscore

'''
