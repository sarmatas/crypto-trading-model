#!/Work/anaconda3/envs/crypto/bin/python

#-----------------------------------------------------------------------
# BitcoinCharts.py
#
#	Various exchange related data from bitcoincharts API.
#
#-----------------------------------------------------------------------
import os
import os.path
import sys
import json
import requests
import pprint
import stat
import shutil
import datetime

url = 'http://api.bitcoincharts.com/v1/markets.json'

# Default outpath for all database
OUT_PATH = "/Work/db"

# Date path, file extensions
T        = datetime.datetime.now()
cur_path = bl.TimeStampDatePath(T)
cur_ext  = bl.TimeStampFileExtension(T)

#
# Get active exchanges
#
F = open('/Work/db/lst/usd_exchange.lst','r')
EXCH = {}
for line in F:
	L = line.split()
	S = L[0] + "USD"
	EXCH[S] = L[1]
F.close()

#
# Download data
#
request  = requests.get(url)

#
# JSON output
#
file1  = OUT_PATH + "/" + cur_path + "/" + "bcharts.exch.json." + cur_ext
file2  = OUT_PATH + "/cur" + "/bcharts.exch.json"
F = open(file1,'w')
F.write(request.text)
F.close()

if (os.path.isfile(file1)):
	os.chmod(file1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(file1,file2)

#
# pprint
#
file1  = OUT_PATH + "/" + cur_path + "/" + "bcharts.exch.pp." + cur_ext
file2  = OUT_PATH + "/cur" + "/bcharts.exch.pp"
data  = json.loads(request.text)
S     = pprint.pformat(data)
F = open(file1,'w')
F.write(S)
F.close()

if (os.path.isfile(file1)):
	os.chmod(file1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(file1,file2)

#
# Text outupt
#
file1  = OUT_PATH + "/" + cur_path + "/" + "bcharts.exch.dat." + cur_ext
file2  = OUT_PATH + "/cur" + "/bcharts.exch.dat"
F = open(file1,'w')

for d in data:
	if (d['symbol'] in EXCH):
		S = "%-10s %8.2f  %8.2f  %8.2f %12.0f\n" % (EXCH[d['symbol']],
		            float(d['close']),float(d['bid']),
		            float(d['ask']),  float(d['currency_volume']))
		F.write(S)
F.close()

if (os.path.isfile(file1)):
	os.chmod(file1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(file1,file2)
