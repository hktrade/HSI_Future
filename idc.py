import requests,logging,time
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import csv,os,os.path
import alpaca_trade_api as tradeapi
import urllib.request,requests
from urllib import error, parse

	
def isnum(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def get_owner(symbol):
	owner=''
	for i,key in enumerate(symbol):
		if isnum(key):
			owner=symbol[0:i]
			break
	return(owner)
	
def get_type(symbol):
	type=''
	for i,key in enumerate(symbol):
		if i>2 and isnum(key)==False and isnum(symbol[i-1])==True:
			if symbol[i]=='C':type='CALL'
			if symbol[i]=='P':type='PUT'
			break
	return(type)
