#!/Work/anaconda3/envs/crypto/bin/python

#-----------------------------------------------------------------------
# Binance.py
#
#	Wrapper to access Binance API functions in BinanceLib.py. Intended
#   for command line or cron.
#   
#   Provides access to all account information, balances, trade history,
#   open orders, etc. Not intended for trading, but includes function
#   call to cancel all outstanding errors.
# 		
#-----------------------------------------------------------------------
import os
import stat
import sys
import json
import time
import datetime
import shutil
import BinanceLib as bl

if (len(sys.argv) !=  2):
	print('Usage:  [ACTION]')
	print('Actions:')
	print('\tGET_ACCOUNT_INFO')
	print('\tGET_ACCOUNT_STATUS')
	print('\tGET_DEPOSIT_HISTORY')
	print('\tGET_WITHDRAW_HISTORY')
	print('\tGET_EXCHANGE_INFO')
	print('\tGET_PRICES')
	print('\tGET_POSITIONS')
	print('\tGET_TRADES')
	print('\tGET_ALL_ORDERS')
	print('\tGET_OPEN_ORDERS')
	print('\tCANCEL_OPEN_ORDERS')
	sys.exit()
	
ACTION = sys.argv[1]

#
# Load trading universe
#
UNIV = "/Work/trd/binance/config/univ.lst"

#
# Set paths
#
T = datetime.datetime.now()
CUR_PATH     = "/Work/trd/binance/cur"
DATE_PATH    = "/Work/trd/binance/" + bl.TimeStampDatePath(T)
DB_CUR_PATH  = "/Work/db/cur"
DB_DATE_PATH = "/Work/db/" + bl.TimeStampDatePath(T)

#
# Move to current path
#
os.chdir(CUR_PATH)

#
# Open Log
#

# Paths are cleaned daily, first append creates new log file
LOG = open('daily.log','a')

# Logging done in library functions, not here
#LOG.write(bl.TimeStamp() + "\n")

#
# Load Universe
#
IN = open(UNIV)
univ = IN.readlines()
for k, u in enumerate(univ):
	univ[k] = univ[k].strip()
IN.close()

#
# Actions
#
if(ACTION == "GET_ACCOUNT_INFO"):
	F1 = CUR_PATH  + "/account.info"
	F2 = DATE_PATH + "/account.info"
	bl.GET_ACCOUNT_INFO(LOG,F1)
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)

elif(ACTION == "GET_ACCOUNT_STATUS"):
	F1 = CUR_PATH  + "/account.status"
	F2 = DATE_PATH + "/account.status"
	bl.GET_ACCOUNT_STATUS(LOG,F1)
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)

elif(ACTION == "GET_DEPOSIT_HISTORY"):
	F1 = CUR_PATH  + "/deposit.history"
	F2 = DATE_PATH + "/deposit.history"
	bl.GET_DEPOSIT_HISTORY(LOG,F1)
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)
	# Json output
	F1 = CUR_PATH  + "/deposit.history.json"
	F2 = DATE_PATH + "/deposit.history.json"
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copyfile(F1,F2)
elif(ACTION == "GET_WITHDRAW_HISTORY"):
	F1 = CUR_PATH  + "/withdraw.history"
	F2 = DATE_PATH + "/withdraw.history"
	bl.GET_WITHDRAW_HISTORY(LOG,F1)
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)
	F1 = CUR_PATH  + "/withdraw.history.json"
	F2 = DATE_PATH + "/withdraw.history.json"
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)
elif(ACTION == "GET_EXCHANGE_INFO"):

	A1 = DB_CUR_PATH + "/binance.exch.json"
	B1 = DB_CUR_PATH + "/binance.exch.info"
	C1 = DB_CUR_PATH + "/binance.stk.info"

	A2 = DB_DATE_PATH + "/binance.exch.json"
	B2 = DB_DATE_PATH + "/binance.exch.info"
	C2 = DB_DATE_PATH + "/binance.stk.info"

	bl.GET_EXCHANGE_INFO(LOG,A1,B1,C1)

	os.chmod(A1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(A1,A2)
	os.chmod(B1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(B1,B2)
	os.chmod(C1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(C1,C2)

elif(ACTION == "GET_PRICES"):
	F1 = CUR_PATH + "/binance.prc"
	S2 = bl.TimeStampFileExtension()
	F2 = DATE_PATH + "/binance." + S2
	bl.GET_TICKERS(LOG,F1)
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)

elif(ACTION == "GET_POSITIONS"):
	F1 = CUR_PATH + "/pos"
	F2 = DATE_PATH + "/pos"
	bl.GET_POSITIONS(LOG,F1)
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)
	F1 = CUR_PATH + "/pos.json"
	F2 = DATE_PATH + "/pos.json"
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)
elif(ACTION == "GET_TRADES"):
	F1 = CUR_PATH + "/trade.history"
	F2 = DATE_PATH + "/trade.history"
	bl.GET_TRADES(LOG,univ,F1)
	os.chmod(F1,stat.S_IWUSR | stat.S_IRUSR)
	shutil.copy(F1,F2)
elif(ACTION == "GET_ALL_ORDERS"):
	F1 = CUR_PATH + "/all_orders.b"
	F2 = DATE_PATH + "/all_orders.b"
	bl.GET_ALL_ORDERS(LOG,univ,F1)
	shutil.copy(F1,F2)

elif(ACTION == "GET_OPEN_ORDERS"):
	F1 = CUR_PATH + "/open_orders.b"
	F2 = DATE_PATH + "/open_orders.b"
	bl.GET_OPEN_ORDERS(LOG,univ,F1)
	shutil.copy(F1,F2)

elif(ACTION == "CANCEL_OPEN_ORDERS"):
	F1 = CUR_PATH + "/cancel_open_orders.b"
	F2 = DATE_PATH + "/cancel_open_orders.b"
	bl.CANCEL_OPEN_ORDERS(LOG,univ,F1)
	shutil.copy(F1,F2)
else:
	LOG.write("Binance.py - INVALID ARGUMENT " + ACTION + "\n")

LOG.close()
