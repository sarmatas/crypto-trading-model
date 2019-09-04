#!/Work/anaconda3/envs/crypto/bin/python

#-----------------------------------------------------------------------
# CoinCapAPI.py
#
# 	Gets data from coincap.io/front and parses out fields for each coin:
#		Symbol
#		Name (with spaces)
#		Market Cap (price * total_supplay)
#		Bitcoin Price
#       USD Price
#		24 hour percent change
# 		Volume
#
#	Output to current working directory and copied to database path.
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

# Default outpath for all database
OUT_PATH = "/Work/db"

# Date path, file extensions
T   = datetime.datetime.now()

cur_path  = bl.TimeStampDatePath(T)
cur_ext   = bl.TimeStampFileExtension(T)

#
# front
#
file1   = OUT_PATH + "/cur" + "/coincap.front.json"
file2   = OUT_PATH + "/cur" + "/coincap.front"
ufile   = OUT_PATH + "/cur" + "/coincap.lst"

url     = 'http://coincap.io/front'

request = requests.get(url)

F = open(file1,'w')
F.write(request.text)
F.close()

data = json.loads(request.text)

F = open(file2,'w')
S = 'Sym\tName\tMktCap\tUsdPrice\tBtcPrice\t24hPctChg\tVolume\n'
F.write(S)

FUNIV = open(ufile,'w')

btc_price = 1.0
for d in data:
	d['price']  = float(d['price'])
	d['mktcap'] = float(d['mktcap'])
	d['perc']   = float(d['perc']) / 100.0
	d['volume'] = float(d['volume'])
	if (d['short'] == "BTC"):
		btc_price = float(d['price'])

for d in data:
	S = '%s\t%s\t' % (d['short'],d['long'])
	F.write(S)
	x = d['price'] / btc_price
	S = '%.0f\t%.5f\t%.8f\t%.5f\t%.0f\n' % ( d['mktcap'],
	         d['price'], x, d['perc'], d['volume'])
	F.write(S)
	S = "%s\n" % (d['short'])
	FUNIV.write(S)
F.close()	
FUNIV.close()

file3   = OUT_PATH + "/" + cur_path + "/" + "coincap.front.json." + cur_ext
file4   = OUT_PATH + "/" + cur_path + "/" + "coincap.front." + cur_ext
ufile2  = OUT_PATH + "/" + cur_path + "/" + "coincap.lst"

if (os.path.isfile(file1)):
	os.chmod(file1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(file1,file3)

if (os.path.isfile(file2)):
	os.chmod(file1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(file2,file4)

if (os.path.isfile(ufile)):
	os.chmod(ufile,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(ufile,ufile2)

#
# global
#
url    = 'http://coincap.io/global'
request  = requests.get(url)

file1  = OUT_PATH + "/cur" + "/coincap.global.json"
file2  = OUT_PATH + "/" + cur_path + "/" + "coincap.global.json." + cur_ext
F = open(file1,'w')
F.write(request.text)
F.close()

if (os.path.isfile(file1)):
	os.chmod(file1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(file1,file2)

