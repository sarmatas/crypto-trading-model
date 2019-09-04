#!/Work/anaconda3/envs/crypto/bin/python

#-----------------------------------------------------------------------
# CoinMarketCapTicker.py
#
# Access coinmarketcap.com API for list of tickers.
#
#-----------------------------------------------------------------------
import sys
import json
import requests

file_name = sys.argv[1]
base_url  = 'https://api.coinmarketcap.com/v1/'
url       = '%s%s' % (base_url,'ticker/')
params    = {'start': 1, "limit" : 1000}
request   = requests.get(url,params)
data      = request.json()

n = 0
f = open(file_name,"w")
for t in data:
	if (n==0):
		for key, value in t.items():
			f.write(key)
			f.write("\t")
		f.write("\n")	
		n = 999
	for key, value in t.items():
		f.write('%s' % value)
		f.write("\t")
	f.write("\n")
f.close()	
