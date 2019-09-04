#!/Work/anaconda3/envs/crypto/bin/python

#-----------------------------------------------------------------------
# BinanceGetPrices.py
#
#	Gets live prices from Binance API.
#
#	Creates cur.prc, prv.prc and 24h.prc in working path. cur.prc is the most
#   recent prices, prv.prc is T - DELTA period price, and 24h.prc is the price
#   exactly 24 hours ago. These files allow any other program to access 
#	current prices without having to do time or date calculations. 
#
#   Also creates json formats of above files: cur.json, prv.json, 24h.json
#
#	Work flow:
#
#		1.) Get current prices from binance API and save to database. 
#           Database is simply text files organized as:
#				/YYYY/MM/DD/filename.HHMM, ex. /2019/05/13/binance.2335
#           
#		2.) Copy most recent prices from database to working path: 
#				cp /YYYY/MM/DD/binance.2335 /Work/cur/cur.prc
#   
#		3.) Copy previous period to working path:
#				cp /YYYY/MM/DD/binance.2325 /Work/cur/prv.prc 
#				(time DELTA == 10 minutes)
#
#		4.) Copy file 24 hours ago to working path:
#				cp /YYYY/MM/DD-1/binance.2335 /Work/cur/24h.prc
#
#		5.) Create JSON format files in working path:
#				/Work/cur/cur.json prv.json, 24h.json
#
#-----------------------------------------------------------------------

import os
import os.path
import stat
import shutil
import sys
import datetime
import BinanceLib as bl

# Default outpath for all database
OUT_PATH = "/Work/db"

# Log File
LOG_FILE  = OUT_PATH + "/cur/binance.log"

LOG = open(LOG_FILE,'a')

LOG.write("BinanceGetPrices\n")

#
# Date path, file extensions
#
T   = datetime.datetime.now()
D   = datetime.timedelta(minutes=10)
TT  = T - D
D   = datetime.timedelta(days=1)
TTT = T - D

cur_path  = bl.TimeStampDatePath(T)
prv_path  = bl.TimeStampDatePath(TT)
prd_path  = bl.TimeStampDatePath(TTT)

cur_ext   = bl.TimeStampFileExtension(T)
prv_ext   = bl.TimeStampFileExtension(TT)
prd_ext   = bl.TimeStampFileExtension(TTT)

cur_file  = OUT_PATH + "/" + cur_path + "/" + "binance." + cur_ext
cur_file2 = OUT_PATH + "/cur" + "/cur.prc"

prv_file  = OUT_PATH + "/" + prv_path + "/" + "binance." + prv_ext
prv_file2 = OUT_PATH + "/cur" + "/prv.prc"

prd_file  = OUT_PATH + "/" + prd_path + "/" + "binance." + prd_ext
prd_file2 = OUT_PATH + "/cur" + "/24h.prc"

# 
# Update Log
#
S = "\tcur_file:  %s\n"   % (cur_file)
LOG.write(S)

S = "\tprv_file:  %s\n"   % (prv_file)
LOG.write(S)

S = "\tprd_file:  %s\n\n" % (prd_file)
LOG.write(S)

#
# Get current prices
#
bl.GET_TICKERS(LOG,cur_file)

os.chmod(cur_file,stat.S_IWUSR | stat.S_IRUSR)

if (os.path.isfile(cur_file)):
	shutil.copy(cur_file,cur_file2)

#
# Get previous prices
#
if (os.path.isfile(prv_file)):
	shutil.copy(prv_file,prv_file2)
else:
	S = "\tERROR - File Missing: %s\n" % (prv_file)
	LOG.write(S)

if (os.path.isfile(prd_file)):
	shutil.copy(prd_file,prd_file2)
else:
	S = "\tERROR - File Missing: %s\n" % (prd_file)
	LOG.write(S)

#
# Create json files
#
cur_json = OUT_PATH + "/cur" + "/cur.prc.json"
prv_json = OUT_PATH + "/cur" + "/prv.prc.json"
prd_json = OUT_PATH + "/cur" + "/24h.prc.json"

if (os.path.isfile(cur_file2)):
	bl.ConvertPrcToJson(cur_file2,cur_json)
	os.chmod(cur_json,stat.S_IWUSR | stat.S_IRUSR)

if (os.path.isfile(prv_file2)):
	bl.ConvertPrcToJson(prv_file2,prv_json)
	os.chmod(prv_json,stat.S_IWUSR | stat.S_IRUSR)

if (os.path.isfile(prd_file2)):
	bl.ConvertPrcToJson(prd_file2,prd_json)
	os.chmod(prd_json,stat.S_IWUSR | stat.S_IRUSR)


LOG.close()
