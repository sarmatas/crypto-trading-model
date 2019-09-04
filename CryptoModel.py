#!/Work/anaconda3/envs/crypto/bin/python

#-----------------------------------------------------------------------
# CryptoModel.py
#
#	Implemention of equity style, portfolio based statistical arbitrage
#	model in crypto space.
#
#	This version is a simple continously rebalanced long book which
#	would be expected to capture volatility through market mean-reversion.
#
#-----------------------------------------------------------------------
import os
import os.path
import stat
import shutil
import sys
import datetime
import time
import json
import pprint
from copy import copy
import BinanceLib as bl

if (len(sys.argv) !=  6):
	print('Usage:  CONFIG_FILE  ACTION [INIT,RBL,CXL] BUY_FLAG [T,F] SELL_FLAG [T,F] TRADE_FLAG [LIVE,TEST]')
	sys.exit()

config_file  = sys.argv[1]
ACTION       = sys.argv[2]
BUY_FLAG     = sys.argv[3]
SELL_FLAG    = sys.argv[4]
TRADE_FLAG   = sys.argv[5]

BUY_FLAG = BUY_FLAG.upper()
SELL_FLAG = SELL_FLAG.upper()

if (BUY_FLAG == 'T'):
	BUY_FLAG = 'TRUE'
	
if (BUY_FLAG == 'F'):
	BUY_FLAG = 'FALSE'
	
if (SELL_FLAG == 'T'):
	SELL_FLAG = 'TRUE'
	
if (SELL_FLAG == 'F'):
	SELL_FLAG = 'FALSE'
	
if (ACTION != "INIT" and ACTION != "RBL" and ACTION != "CXL"):
	S = "INVALID ACTION:  %s\n" % (ACTION)
	print(S)
	sys.exit()

if (TRADE_FLAG != "LIVE" and TRADE_FLAG != "TEST"):
	S = "INVALID TRADE_FLAG:  %s\n" % (TRADE_FLAG)
	print(S)
	sys.exit()

#
# Constants
#
TRD_BASE_PATH  = '/Work/trd'
DB_BASE_PATH   = '/Work/db'

#
# TimeStamps
#
T        = datetime.datetime.now()
TS       = bl.TimeStamp()
EXT      = bl.TimeStampFileExtension(T)
LEXT     = bl.TimeStampFileExtension(T)
CUR_TIME = bl.TimeStampIntTime(T)

D  = datetime.timedelta(days=1)
TT = T - D
cur_db_path   = DB_BASE_PATH + "/" + bl.TimeStampDatePath(T)
prv_db_path   = DB_BASE_PATH + "/" + bl.TimeStampDatePath(TT)
cur_trd_path  = TRD_BASE_PATH + "/binance" + "/" + bl.TimeStampDatePath(T)
prv_trd_path  = TRD_BASE_PATH + "/binance" + "/" + bl.TimeStampDatePath(TT)
cur_db_ext    = bl.TimeStampFileExtension(T)
prv_db_ext    = bl.TimeStampFileExtension(TT)

#
# Load Parameters
#
if not os.path.isfile(config_file):
	S = "MISSING FILE:  %s" % (config_file)
	print(S)
	sys.exit()
	
par = bl.LoadConfig(config_file)

par['HEDGE_RATIO'] = float(par['HEDGE_RATIO'])
par['CAPITAL']     = float(par['CAPITAL'])
MAX_ORDERS         = int(par['MAX_ORDERS'])
ORDER_DELAY   	   = float(par['ORDER_DELAY'])
MIN_ORDER_MV   	   = float(par['MIN_ORDER_MV'])
BASE_CURRENCY  	   = par['BASE_CURRENCY']

#
# Set Paths
#
PORTFOLIO_PATH   = TRD_BASE_PATH  + '/' + 	par['EXCHANGE_NAME'] + '/' +  par['PORTFOLIO_NAME']
										
DATABASE_PATH    = DB_BASE_PATH + '/cur'
					
CONFIG_PATH      = PORTFOLIO_PATH + '/config'

TRADE_PATH       = PORTFOLIO_PATH + '/cur'
					
UNIV_FILE        = CONFIG_PATH + '/univ.lst'

RESTRICTED_FILE  = CONFIG_PATH + '/restricted.lst'

PRV_DAY_PRC_FILE = prv_db_path + '/binance.1245' 

PRV_PRC_FILE     = DATABASE_PATH + '/prv.prc.json'

CUR_PRC_FILE     = DATABASE_PATH + '/cur.prc.json'

DAT_FILE         = DATABASE_PATH + '/binance.dat'

POSITION_FILE    = TRADE_PATH + '/pos'

PRV_POS_FILE     = prv_trd_path + '/pos'

#
# Open Log Files
#
S = TRADE_PATH + "/t.log"
TLOG = open(S,'a')

S = TRADE_PATH + "/v.log"
VLOG = open(S,'a')

S = TRADE_PATH + "/error.log"
ERR = open(S,'w')

S = "Verbose Log -- %s\n\n" % (TS)
VLOG.write(S)

S = "Error Log -- %s\n\n" % (TS)
ERR.write(S)

#
# Check Files
#
FILES = [UNIV_FILE,RESTRICTED_FILE,PRV_PRC_FILE,CUR_PRC_FILE,DAT_FILE,
         POSITION_FILE,PRV_DAY_PRC_FILE,PRV_POS_FILE]
N = 0
for file in FILES:
	if not os.path.isfile(file):
		S = "MISSING FILE:  %s\n" % (file)
		ERR.write(S)
		N += 1
if (N > 0):		
	sys.exit()

#
# VLOG
#
VLOG.write("Argv:\n\n") 
S = "\t%s %s %s %s %s %s\n" % (sys.argv[0], sys.argv[1], sys.argv[2],
                               sys.argv[3], sys.argv[4], sys.argv[5])
VLOG.write(S)

VLOG.write("\nPaths:\n\n") 

S = "\tPORTFOLIO_PATH:   %s\n" % (PORTFOLIO_PATH)
VLOG.write(S)

S = "\tDATABASE_PATH:    %s\n" % (DATABASE_PATH)
VLOG.write(S)

S = "\tCONFIG_PATH:      %s\n" % (CONFIG_PATH)
VLOG.write(S)

S = "\tTRADE_PATH:       %s\n" % (TRADE_PATH)
VLOG.write(S)

S = "\tcur_db_path:      %s\n" % (cur_db_path)
VLOG.write(S)

S = "\tprv_db_path:      %s\n" % (prv_db_path)
VLOG.write(S)

S = "\tcur_trd_path:     %s\n" % (cur_trd_path)
VLOG.write(S)

S = "\tprv_trd_path:     %s\n" % (prv_trd_path)
VLOG.write(S)

VLOG.write("\nFiles:\n\n") 

S = "\tUNIV_FILE:        %s\n" % (UNIV_FILE)
VLOG.write(S)

S = "\tRESTRICTED_FILE:  %s\n" % (RESTRICTED_FILE)
VLOG.write(S)

S = "\tPRV_PRC_FILE:     %s\n" % (PRV_PRC_FILE)
VLOG.write(S)

S = "\tCUR_PRC_FILE:     %s\n" % (CUR_PRC_FILE)
VLOG.write(S)

S = "\tPRV_DAY_PRC_FILE: %s\n" % (PRV_DAY_PRC_FILE)
VLOG.write(S)

S = "\tPOSITION_FILE:    %s\n" % (POSITION_FILE)
VLOG.write(S)

S = "\tPRV_POS_FILE:     %s\n" % (PRV_POS_FILE)
VLOG.write(S)

S = "\tDAT_FILE:         %s\n" % (DAT_FILE)
VLOG.write(S)

VLOG.write("\nParameters:\n\n") 

S = "\tHEDGE_RATIO:      %f\n" % (par['HEDGE_RATIO'])
VLOG.write(S)
				
S = "\tCAPITAL:          %f\n" % (par['CAPITAL'])
VLOG.write(S)

VLOG.write("\nConstants:\n\n") 

S = "\tORDER_DELAY:      %f\n" % (ORDER_DELAY)
VLOG.write(S)

S = "\tBASE_CURRENCY:    %s\n" % (BASE_CURRENCY)
VLOG.write(S)

S = "\tMIN_ORDER_MV:     %f\n" % (MIN_ORDER_MV)
VLOG.write(S)

S = "\tMAX_ORDERS:       %d\n" % (MAX_ORDERS)
VLOG.write(S)

#
# File Dates and Sizes
#
VLOG.write("\n\nFile Time and Size:\n")
for F in FILES:
	mtime    = os.path.getmtime(F)
	T = datetime.datetime.fromtimestamp(mtime)
	S1 = bl.TimeStamp2(T)
	statinfo = os.stat(F)
	S2 = "\t%-60s    %s    %d\n" % (F,S1,statinfo.st_size)
	VLOG.write(S2)

#
# Load Universe
#
IN = open(UNIV_FILE)
UNIV = IN.readlines()
univ = []
for k, u in enumerate(UNIV):
	sym     = UNIV[k].strip()
	if (len(sym) < 2):
		continue
	univ.append(sym)
IN.close()

VLOG.write("\nUniverse:\n\n") 
S = "\tNumber:        %d\n" % (len(univ))
VLOG.write(S)

#
# Load Restricted
#
IN = open(RESTRICTED_FILE)
RESTRICTED = IN.readlines()
restricted = []
for k, u in enumerate(RESTRICTED):
	sym     = RESTRICTED[k].strip()
	if (len(sym) < 2):
		continue
	restricted.append(sym)
IN.close()

VLOG.write("\nRestricted:\n\n") 
S = "\tNumber:       %d\n" % (len(restricted))
VLOG.write(S)
VLOG.write("\t\tList:\n")
for r in restricted:
	S = "\t\t%s\n" % (r)
	VLOG.write(S)

#
# Create data
#
data = {}

for u in univ:
	rec = {'sym'        : u,   
	       'pos'        : 0.0, 'prv_pos'     : 0.0, 'mv'    : 0.0,
	       'Prv'        : 0.0, 'Last'        : 0.0, 'PrvDay': 0.0,
	       'ret'        : 0.0, 'ret_prv_day' : 0.0,
	       'Rank'       : 0.0, 'MktCap'      : 0.0, 'LotSize' : 0.0,
	       'TickSize'   : 0.0, 'USvol24'     : 0.0,
	       'target_mv'  : 0.0, 'target_qty'  : 0.0, 
	       'trade_mv'   : 0.0, 'trade_qty'   : 0.0, 
	       'fills'      : 0.0, 'Side'        : 'NA',
	       'rv'         : 'NA' }

	data[u] = copy(rec)
	
#
# Load positions
#
F = open(POSITION_FILE,'r')
for line in F:
	L = line.split()
	if (L[0] in data):
		data[L[0]]['pos'] = float(L[1])
F.close()

F = open(PRV_POS_FILE,'r')
for line in F:
	L = line.split()
	if (L[0] in data):
		data[L[0]]['prv_pos'] = float(L[1])
F.close()

#
# Load prices
#

# Copy to local path before opening
LOCAL_FILE = TRADE_PATH + "/cur.prc.json"
shutil.copy(CUR_PRC_FILE,LOCAL_FILE)

IN  = open(LOCAL_FILE)
S   = IN.read()
prc = json.loads(S)
for P in prc:
	if (P['Symbol'] in data):
		data[P['Symbol']]['Last'] = float(P['Last'])
		Last = data[P['Symbol']]['Last']
		if (P['Symbol'] == "BTC"):
			BTC_PRC = Last
			Last    = 1.0
		data[P['Symbol']]['mv']   = data[P['Symbol']]['pos'] * Last

LOCAL_FILE = TRADE_PATH + "/prv.prc.json"
shutil.copy(PRV_PRC_FILE,LOCAL_FILE)
		
IN  = open(LOCAL_FILE)
S   = IN.read()
prc = json.loads(S)
for P in prc:
	if (P['Symbol'] in data):
		data[P['Symbol']]['Prv'] = float(P['Last'])

LOCAL_FILE = TRADE_PATH + "/prv_day.prc"
shutil.copy(PRV_DAY_PRC_FILE,LOCAL_FILE)

F = open(LOCAL_FILE,'r')
for line in F:
	L = line.split()
	if (L[0] in data):
		data[L[0]]['PrvDay'] = float(L[1])
F.close()

#
# Returns
#
for d in data:
	if (data[d]['Prv'] > 0.0):
		data[d]['ret'] = data[d]['Last'] / data[d]['Prv'] - 1.0
	if (data[d]['PrvDay'] > 0.0):
		data[d]['ret_prv_day'] = data[d]['Last'] / data[d]['PrvDay'] - 1.0

#
# Check Positions
#
N = 0
for d in data:
	dif = data[d]['pos'] - data[d]['prv_pos']
	if (dif > 0.0):
		S = "\tWARNING - Position Difference  sym:  %-8s  prv:  %.8f  cur: %.8f\n" % (d,data[d]['prv_pos'],data[d]['pos'])
		ERR.write(S)
		N += 1
if (N > 0):
	 S = "\tERROR: Too many position differences: %d\n" % (N)
	 ERR.write(S)
	 sys.exit()		
		
#
# Check Prices
#
VLOG.write("\nChecking Prices:\n\n") 
VLOG.write("\tSymbol    Last     Prv     PrvDay\n")

sym = 'BTC'
d = data.get(sym,'NA')
if (d != 'NA'):
	S = "\t%s     %.2f   %.2f  %.2f\n" % (sym,d['Last'],d['Prv'],d['PrvDay'])
	VLOG.write(S)

sym = 'ETH'
d = data.get(sym,'NA')
if (d != 'NA'):
	S = "\t%s     %.8f   %.8f   %.8f\n" % (sym,d['Last'],d['Prv'],d['PrvDay'])
	VLOG.write(S)
	
sym = 'XRP'
d = data.get(sym,'NA')
if (d != 'NA'):
	S = "\t%s     %.8f   %.8f   %.8f\n" % (sym,d['Last'],d['Prv'],d['PrvDay'])
	VLOG.write(S)


PRV_PRC_FILE     = DATABASE_PATH + '/prv.prc.json'

CUR_PRC_FILE     = DATABASE_PATH + '/cur.prc.json'

T_NOW = datetime.datetime.now()
mtime = os.path.getmtime(CUR_PRC_FILE)
T     = datetime.datetime.fromtimestamp(mtime)
D     = T_NOW - T
if (D.seconds > 70):
	S = "\t*** ERROR *** cur.prc file time stamp is old\n" 
	ERR.write(S)
	sys.exit()
	
mtime = os.path.getmtime(PRV_PRC_FILE)
T     = datetime.datetime.fromtimestamp(mtime)
D     = T_NOW - T
if (D.seconds > 70):
	S = "\t*** ERROR *** prv.prc file time stamp is old\n" 
	ERR.write(S)
	sys.exit()
	
N_MISSING     = 0
N_LARGE       = 0
N_LARGE_DAILY = 0
for d in data:
	if (data[d]['Last'] < .000000001):
		N_MISSING += 1
		S = "MISSING PRICE %s\n" % (d)
		ERR.write(S)
	if (abs(data[d]['ret']) > .25):
		N_LARGE += 1
		S = "LARGE RETURN  %s  %.f\n" % (d,data[d]['ret'])
		ERR.write(S)
	if (abs(data[d]['ret_prv_day']) > .25):
		N_LARGE_DAILY += 1
		S = "LARGE PRV DAY RETURN  %s  %.f\n" % (d,data[d]['ret_prv_day'])
		ERR.write(S)
if (N_MISSING > 1 or N_LARGE > 2 or N_LARGE_DAILY > 2):
	S = "\t*** PRICE ERROR *** MISSING: %d  LARGE_RETURNS: %d LARGE_DAILY_RETURNS: %d\n" % (N_MISSING,N_LARGE,N_LARGE_DAILY)
	ERR.write(S)
	sys.exit()

#
# Load Dat
#
F = open(DAT_FILE,'r')
for line in F:
	L = line.split()
	if (L[0] in data):
		data[L[0]]['Rank']     = float(L[1])
		data[L[0]]['MktCap']   = float(L[2])
		data[L[0]]['USvol24']  = float(L[3])
		data[L[0]]['LotSize']  = float(L[6])
		data[L[0]]['TickSize'] = float(L[7])
F.close()

#
# Load Portfolio
#
PORTFOLIO = {'n'                : 0.0, 'mv'                : 0.0, 
	         'target_n'         : 0.0, 'target_mv'         : 0.0, 
             'target_pos_wgt'   : 0.0, 'target_pos_mv'     : 0.0,
             'buy_order_n'      : 0.0, 'buy_order_mv'      : 0.0,
             'buy_order_fills'  : 0.0, 'buy_order_leaves'  : 0.0, 
             'sell_order_n'     : 0.0, 'sell_order_mv'     : 0.0, 
             'sell_order_fills' : 0.0, 'sell_order_leaves' : 0.0,
             'order_n'          : 0.0, 'order_mv'          : 0.0,
             'order_fills'      : 0.0, 'order_leaves'      : 0.0,
             'commissions'      : 0.0}   
			 
for d in data:
	if (data[d]['pos'] > 0.0):
		PORTFOLIO['n']  += 1
		PORTFOLIO['mv'] += data[d]['mv']

if (ACTION == "RBL"):
	PORTFOLIO['target_mv'] = PORTFOLIO['mv'] * par['HEDGE_RATIO']
elif (ACTION == "INIT"):
	PORTFOLIO['target_mv'] = par['CAPITAL'] * par['HEDGE_RATIO']
else:
	sys.exit() # Redundant
	
#
# Calculate
#
N = 0
for d in data:
	if (d in restricted):
		continue	
	if (data[d]['Last'] > 0.0):
		N += 1

PORTFOLIO['target_n']       = N
PORTFOLIO['target_pos_wgt'] = 1 / N
PORTFOLIO['target_pos_mv']  = PORTFOLIO['target_pos_wgt'] * PORTFOLIO['target_mv']

for d in data:
	if (d in restricted):
		continue	
	if (data[d]['Last'] < 0.00000001):
		continue
	data[d]['target_mv']  = PORTFOLIO['target_pos_mv']
	data[d]['target_qty'] = PORTFOLIO['target_pos_mv'] / data[d]['Last']
	data[d]['target_qty'] = bl.RoundShares(data[d]['target_qty'], data[d]['LotSize'])
	data[d]['trade_qty']  = data[d]['target_qty'] - data[d]['pos']
	data[d]['trade_mv']   = abs(data[d]['trade_qty']) * data[d]['Last']
	if (data[d]['trade_mv'] < MIN_ORDER_MV):
		data[d]['Side'] = 'LT_MIN_ORDER'
	elif (data[d]['trade_qty'] < 0.0):
		data[d]['Side'] = 'SELL'
		data[d]['trade_qty'] = abs(data[d]['trade_qty'])
	elif (data[d]['trade_qty']) > 0.0:
		data[d]['Side'] = 'BUY'
	data[d]['trade_qty'] = bl.RoundShares(data[d]['trade_qty'], data[d]['LotSize'])

#
# Orders 
#
orders    = {}
orders_rv = {}
rv        = {}
ORDERS    = []

rec    = {'sym'         : 'NA', 'Side' : 'NA', 
          'order_qty'   : 0.0,  'order_mv'  : 0.0,  'order_prc' : 0.0, 
          'executedQty' : 0.0,  'net_qty'   : 0.0,
          'fill_qty'    : 0.0,  'fill_mv'   : 0.0,  'fill_prc'  : 0.0,
          'commission'  : 0.0,  'orderId'   : 'NA',
          'origQty'     : 0.0,  'leaves'    : 0.0,
          'status'      : 'NA', 'symbol'    : 'NA',
          'timeInForce' : 'NA', 'ts'        : 'NA',
          'type'        : 'NA'}          

for d in data:
	rec['sym'] = d + BASE_CURRENCY
	orders[d]  = copy(rec)

#
# Sell Orders
#	
if (SELL_FLAG == "TRUE"):
	N = 0
	for d in data:
		if (data[d]['Side'] != 'SELL'):
			continue
		if (N >= MAX_ORDERS):
			break
		sym   = d + BASE_CURRENCY
		sh    = data[d]['trade_qty']
		side  = data[d]['Side']

		rec['sym']        = sym
		rec['Side']       = side
		rec['order_qty']  = sh
		rec['order_prc']  = data[d]['Last']
		rec['order_mv']   = sh * data[d]['Last']
	
		if (TRADE_FLAG == "LIVE"):
			rv = bl.SEND_MARKET_ORDER(TLOG,sym,sh,side)	
			orders_rv[d] = rv
			for F in rv['fills']:
				rec['fill_qty']   = float(F['qty'])
				rec['fill_mv']    = float(F['price']) * float(F['qty'])
				rec['commission'] = float(F['commission'])
			rec['executedQty']  = float(rv['executedQty'])
			rec['net_qty']      = rec['executedQty'] - rec['commission']
			rec['orderId']      = rv['orderId']
			rec['origQty']      = float(rv['origQty'])
			rec['leaves']       = rec['origQty'] = rec['executedQty']
			rec['status']       = rv['status']
			rec['symbol']       = rv['symbol']
			rec['timeInForce']  = rv['timeInForce']
			rec['ts']           = rv['transactTime']
			rec['type']         = rv['type']
			
		PORTFOLIO['sell_order_n']      += 1
		PORTFOLIO['sell_order_mv']     += rec['order_mv']
		PORTFOLIO['sell_order_fills']  += rec['fill_mv']
		PORTFOLIO['sell_order_leaves'] += rec['order_mv'] - rec['fill_mv'] 
		PORTFOLIO['commissions']       += rec['commission']

		REC = copy(rec)
		orders[d] = REC	
		ORDERS.append(REC)
		time.sleep(ORDER_DELAY)
		N += 1

#
# Buy Orders
#
if (BUY_FLAG == "TRUE"):
	N = 0
	for d in data:
		if (data[d]['Side'] != 'BUY'):
			continue
		if (N >= MAX_ORDERS):
			break
		sym   = d + BASE_CURRENCY
		sh    = data[d]['trade_qty']
		side  = data[d]['Side']

		rec['sym']        = sym
		rec['Side']       = side
		rec['order_qty']  = sh
		rec['order_prc']  = data[d]['Last']
		rec['order_mv']   = sh * data[d]['Last']

		if (TRADE_FLAG == "LIVE"):
			rv = bl.SEND_MARKET_ORDER(TLOG,sym,sh,side)	
			orders_rv[d] = rv
			for F in rv['fills']:
				rec['fill_qty']    = float(F['qty'])
				rec['fill_mv']     = float(F['price']) * float(F['qty'])
				rec['commission']  = float(F['commission'])
			rec['executedQty']  = float(rv['executedQty'])
			rec['net_qty']      = rec['executedQty'] - rec['commission']
			rec['orderId']      = rv['orderId']
			rec['origQty']      = float(rv['origQty'])
			rec['leaves']       = rec['origQty'] = rec['executedQty']
			rec['status']       = rv['status']
			rec['symbol']       = rv['symbol']
			rec['timeInForce']  = rv['timeInForce']
			rec['ts']           = rv['transactTime']
			rec['type']         = rv['type']
			
		PORTFOLIO['buy_order_n']      += 1
		PORTFOLIO['buy_order_mv']     += rec['order_mv']
		PORTFOLIO['buy_order_fills']  += rec['fill_mv']
		PORTFOLIO['buy_order_leaves'] += rec['order_mv'] - rec['fill_mv'] 
		PORTFOLIO['commissions']      += rec['commission']

		REC = copy(rec)
		orders[d] = REC	
		ORDERS.append(REC)
		time.sleep(ORDER_DELAY)
		N += 1

PORTFOLIO['order_n']      = PORTFOLIO['buy_order_n'] + PORTFOLIO['sell_order_n']
PORTFOLIO['order_mv']     = PORTFOLIO['buy_order_mv'] + PORTFOLIO['sell_order_mv']
PORTFOLIO['order_fills']  = PORTFOLIO['buy_order_fills'] + PORTFOLIO['sell_order_fills']
PORTFOLIO['order_leaves'] = PORTFOLIO['buy_order_leaves'] + PORTFOLIO['sell_order_leaves']

#
# Output
#
out_file = TRADE_PATH + "/orders_rv.json"
F = open(out_file,'w')
S = json.dumps(orders_rv)
F.write(S)
F.close()

out_file = TRADE_PATH + "/orders_rv.pp"
F = open(out_file,'w')
S = pprint.pformat(orders_rv)
F.write(S)
F.close()

out_file = TRADE_PATH + "/orders.json"
F = open(out_file,'w')
S = json.dumps(ORDERS)
F.write(S)
F.close()

out_file = TRADE_PATH + "/orders.pp"
F = open(out_file,'w')
S = pprint.pformat(ORDERS)
F.write(S)
F.close()

out_file = TRADE_PATH + "/data.json"
S = json.dumps(data)
F = open(out_file,'w')
F.write(S)
F.close()

out_file = TRADE_PATH + "/data.pp"
S = pprint.pformat(data)
F = open(out_file,'w')
F.write(S)
F.close()

out_file = TRADE_PATH + "/port.json"
S = json.dumps(PORTFOLIO)
F = open(out_file,'w')
F.write(S)
F.close()

out_file = TRADE_PATH + "/port.pp"
S = pprint.pformat(PORTFOLIO)
F = open(out_file,'w')
F.write(S)
F.close()

out_file = TRADE_PATH + "/t.data"
F = open(out_file,'w')
S = "data.sym\t"
F.write(S)
S = "data.pos\t"
F.write(S)
S = "data.prv_pos\t"
F.write(S)
S = "data.mv\t"
F.write(S)
S = "data.Prv\t"
F.write(S)
S = "data.Last\t"
F.write(S)
S = "data.PrvDay\t"
F.write(S)
S = "data.ret\t"
F.write(S)
S = "data.ret_prv_day\t"
F.write(S)
S = "data.Rank\t"
F.write(S)
S = "data.MktCap\t"
F.write(S)
S = "data.LotSize\t"
F.write(S)
S = "data.TickSize\t"
F.write(S)
S = "data.USvol24\t"
F.write(S)
S = "data.target_mv\t"
F.write(S)
S = "data.target_qty\t"
F.write(S)
S = "data.trade_mv\t"
F.write(S)
S = "data.trade_qty\t"
F.write(S)
S = "data.fills\t"
F.write(S)
S = "data.Side\t"
F.write(S)
S = "orders.sym\t"
F.write(S)
S = "orders.Side\t"
F.write(S)
S = "orders.order_qty\t"
F.write(S)
S = "orders.order_mv\t"
F.write(S)
S = "orders.order_prc\t"
F.write(S)
S = "orders.executedQty\t"
F.write(S)
S = "orders.net_qty\t"
F.write(S)
S = "orders.fill_qty\t"
F.write(S)
S = "orders.fill_mv\t"
F.write(S)
S = "orders.fill_prc\t"
F.write(S)
S = "orders.commission\t"
F.write(S)
S = "orders.orderId\t"
F.write(S)
S = "orders.origQty\t"
F.write(S)
S = "orders.leaves\t"
F.write(S)
S = "orders.status\t"
F.write(S)
S = "orders.symbol\t"
F.write(S)
S = "orders.timeInForce\t"
F.write(S)
S = "orders.ts\t"
F.write(S)
S = "orders.type\n"
F.write(S)

for d in data:
	S = "%s\t" % (d)
	F.write(S)
	S = "%.8f\t" % (data[d]['pos'])
	F.write(S)
	S = "%.8f\t" % (data[d]['prv_pos'])
	F.write(S)
	S = "%.8f\t" % (data[d]['mv'])
	F.write(S)
	S = "%.8f\t" % (data[d]['Prv'])
	F.write(S)
	S = "%.8f\t" % (data[d]['Last'])
	F.write(S)
	S = "%.8f\t" % (data[d]['PrvDay'])
	F.write(S)
	S = "%.8f\t" % (data[d]['ret'])
	F.write(S)
	S = "%.8f\t" % (data[d]['ret_prv_day'])
	F.write(S)
	S = "%.8f\t" % (data[d]['Rank'])
	F.write(S)
	S = "%.8f\t" % (data[d]['MktCap'])
	F.write(S)
	S = "%.8f\t" % (data[d]['LotSize'])
	F.write(S)
	S = "%.8f\t" % (data[d]['TickSize'])
	F.write(S)
	S = "%.8f\t" % (data[d]['USvol24'])
	F.write(S)
	S = "%.8f\t" % (data[d]['target_mv'])
	F.write(S)
	S = "%.8f\t" % (data[d]['target_qty'])
	F.write(S)
	S = "%.8f\t" % (data[d]['trade_mv'])
	F.write(S)
	S = "%.8f\t" % (data[d]['trade_qty'])
	F.write(S)
	S = "%.8f\t" % (data[d]['fills'])
	F.write(S)
	S = "%s\t"   % (data[d]['Side'])
	F.write(S)
	S = "%s\t"   % (orders[d]['sym'])
	F.write(S)
	S = "%s\t"   % (orders[d]['Side'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['order_qty'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['order_mv'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['order_prc'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['executedQty'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['net_qty'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['fill_qty'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['fill_mv'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['fill_prc'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['commission'])
	F.write(S)
	S = "%s\t"   % (orders[d]['orderId'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['origQty'])
	F.write(S)
	S = "%.8f\t" % (orders[d]['leaves'])
	F.write(S)
	S = "%s\t"   % (orders[d]['status'])
	F.write(S)
	S = "%s\t"   % (orders[d]['symbol'])
	F.write(S)
	S = "%s\t"   % (orders[d]['timeInForce'])
	F.write(S)
	S = "%s\t"   % (orders[d]['ts'])
	F.write(S)
	S = "%s\n"   % (orders[d]['type'])
	F.write(S)
F.close()

#
# Copy Files
#
if (TRADE_FLAG == "LIVE"):

	in_file  = TRADE_PATH + "/t.log"
	out_file = TRADE_PATH + "/t.log" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/v.log"
	out_file = TRADE_PATH + "/v.log" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/error.log"
	out_file = TRADE_PATH + "/error.log" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/t.data"
	out_file = TRADE_PATH + "/t.data" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/cur.prc.json"
	out_file = TRADE_PATH + "/cur.prc.json" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/prv.prc.json"
	out_file = TRADE_PATH + "/prv.prc.json" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/prv.prc.json"
	out_file = TRADE_PATH + "/prv.prc.json" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/prv_day.prc"
	out_file = TRADE_PATH + "/prv_day.prc" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/orders_rv.json"
	out_file = TRADE_PATH + "/orders_rv.json" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file  = TRADE_PATH + "/orders_rv.pp"
	out_file = TRADE_PATH + "/orders_rv.pp" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file = TRADE_PATH + "/orders.json"
	out_file = TRADE_PATH + "/orders.json" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file = TRADE_PATH + "/orders.pp"
	out_file = TRADE_PATH + "/orders.pp" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file = TRADE_PATH + "/data.json"
	out_file = TRADE_PATH + "/data.json" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file = TRADE_PATH + "/data.pp"
	out_file = TRADE_PATH + "/data.pp" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file = TRADE_PATH + "/port.json"
	out_file = TRADE_PATH + "/port.json" + "." + LEXT
	shutil.copy(in_file,out_file)

	in_file = TRADE_PATH + "/port.pp"
	out_file = TRADE_PATH + "/port.pp" + "." + LEXT
	shutil.copy(in_file,out_file)


TLOG.close()
VLOG.close()
