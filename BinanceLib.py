#!/Work/anaconda3/envs/crypto/bin/python

#-----------------------------------------------------------------------
# BinanceLib.py
#
# Wrapper around   https://github.com/sammchardy/python-binance
#
# MIT License
# Copyright (c) 2017 sammchardy
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This library was extremely helpful. I think it also includes multiple
# exchange support.
#
#-----------------------------------------------------------------------
import time
import datetime
import pprint
import json
import os

api_key = 'xxxx'
api_secret = 'xxxx'

from binance.client import Client

# ----------------------------------------------------------------------
# Various time formats
#
def TimeStamp():
	T  = datetime.datetime.now()
	S1 = T.strftime('%Y%m%d-%H:%M:%S.%f') 
	S2 = "%s\n" % (int(time.time() * 1000))
	S  = S1 + "   " + S2
	return S

def TimeStamp2(T):
	S = T.strftime('%Y%m%d-%H:%M') 
	return S

def TimeStampShort():
	S2 = "%s\n" % (int(time.time() * 1000))
	return S2

def TimeStampFileExtension(T):
	S1 = T.strftime('%H%M') 
	return S1

def TimeStampFileExtensionLong(T):
	S1 = T.strftime('%Y%m%d:%H%M') 
	return S1

def TimeStampDatePath(T):
	S1 = T.strftime('%Y/%m/%d') 
	return S1

def TimeStampIntTime(T):
	S = T.strftime('%H%M')
	x = int(S) 
	return x

def TimeStampUnixDate(date_str):
	x = int(int(date_str) / 1000)
	S = datetime.datetime.fromtimestamp(x).strftime('%Y%m%d')
	return S
	
def TimeStampUnixTime(date_str):
	x = int(int(date_str) / 1000)
	S = datetime.datetime.fromtimestamp(x).strftime('%H%M')
	return S

def TimeStampUnixDateTime(date_str):
	x = int(int(date_str) / 1000)
	S = datetime.datetime.fromtimestamp(x).strftime('%Y%m%d:%H%M')
	return S

# ----------------------------------------------------------------------
# LoadConfig
#
def LoadConfig(config_file):
	data = {}
	F = open(config_file,'r')
	for line in F:
		if (line[0] == '#'):
			continue
		L = line.split()
		if (len(L) != 2):
			continue
		A = L[0]
		B = L[1]
		#if (A.find('#')):
			#continue
		data[A] = B
	F.close()
	return(data)

# ----------------------------------------------------------------------
# RoundShares
#
def RoundShares(sh,lot_size):
	lot = 0
	if (lot_size == 1.0):
		lot = 0
	elif (lot_size == .1):
		lot = 1
	elif (lot_size == .01):
		lot = 2
	elif (lot_size == .001):
		lot = 3 
	elif (lot_size == .0001):
		lot = 4
	elif (lot_size == .00001):
		lot = 5	
	elif (lot_size == .000001):
		lot = 6	
	elif (lot_size == .0000001):
		lot = 7	
	elif (lot_size == .00000001):
		lot = 8	
	return round(sh,lot)

# ----------------------------------------------------------------------
# ConvertPrcToJson
#
def ConvertPrcToJson(in_file,out_file):
	data = []
	F = open(in_file,'r')
	for line in F:
		L = line.split()
		rec = {'Symbol' : L[0], 'Last' : L[1], 'Bid' : L[2], 
	       'Ask' : L[3], 'Timestamp' : L[4] }
		data.append(rec)
	F.close()

	S = json.dumps(data)
	F = open(out_file,'w')
	F.write(S)
	F.close()

# ----------------------------------------------------------------------
#
# SEND_MARKET_ORDER
#
def SEND_MARKET_ORDER(LOG,sym,sh,side):
	
	LOG.write("SEND_MARKET_ORDER() " + TimeStamp() + "\n")

	S = "sym: %s  sh: %.8f  side: %s\n" % (sym,sh,side)
	LOG.write(S)
	order = {}

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
	
	try:
		if (side == "SELL"):
			order = client.order_market_sell(symbol=sym,quantity=sh,newOrderRespType="FULL")
		elif (side == "BUY"):
			order = client.order_market_buy(symbol=sym,quantity=sh,newOrderRespType="FULL")

		if (order != None):
			S = pprint.pformat(order)
			LOG.write(S + "\n")

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
	
	return order

# ----------------------------------------------------------------------
#
# SEND_TEST_ORDER
#
def SEND_TEST_ORDER(LOG,trd_file):
	LOG.write("SEND_BASKET() " + TimeStamp() + "\n")

	sym = "ADABTC"
	sh  = 10
	FTRD = open(trd_file,'a')

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
	
	try:
		#order = client.order_market_sell(symbol=sym,quantity=sh)
		order = client.order_market_buy(symbol=sym,quantity=sh,newOrderRespType="FULL")

		if (order != None):
			S = pprint.pformat(order)
			LOG.write(S + "\n")
			if (order['status'] == "FILLED"):
				sym = sym[0:3]
				S = "%s\t%s\n" % (sym,order['origQty'])
				FTRD.write(S)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
	
	FTRD.close()

# ----------------------------------------------------------------------
# GET_ACCOUNT_INFO
#
#   Call:     get_account()
# 
def GET_ACCOUNT_INFO(LOG,acc_file):

	LOG.write("GET_ACCOUNT_INFO() " + TimeStamp() + "\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	try:
		data = client.get_account()

		# Account Info
		F1 = open(acc_file,'w')
		S = "makerCommission \t %s\n" % (data['makerCommission'])
		F1.write(S)
		S = "takerCommission \t %s\n" % (data['takerCommission'])
		F1.write(S)
		S = "buyerCommission \t %s\n" % (data['buyerCommission'])
		F1.write(S)
		S = "sellerCommission \t %s\n" % (data['sellerCommission'])
		F1.write(S)
		S = "canTrade \t %s\n" % (data['canTrade'])
		F1.write(S)
		S = "canWithdraw \t %s\n" % (data['canWithdraw'])
		F1.write(S)
		S = "canDeposit \t %s\n" % (data['canDeposit'])
		F1.write(S)
		S = "updateTime \t %s\n" % (data['updateTime'])
		F1.write(S)
		F1.close()

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")

# ----------------------------------------------------------------------
# GET_ACCOUNT_STATUS
#
#        get_account_status(self, **params):
#
#        	: param recvWindow: the number of milliseconds the request is valid for
#        	: type recvWindow: int
#        	: returns:
#            {
#                "msg": "Order failed:Low Order fill rate! Will be reactivated after 5 minutes.",
#                "success": true,
#                "objs": [
#                    "5"
#                ]
#            }
#
def GET_ACCOUNT_STATUS(LOG,out_file):

	LOG.write("GET_ACCOUNT_STATUS() " + TimeStamp() + "\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	try:
		data = client.get_account_status()

		# Account Info
		F1 = open(out_file,'w')
		S = "msg:            \t%s\n" % (data['msg'])
		F1.write(S)
		S = "success         \t%s\n" % (data['success'])
		F1.write(S)
		F1.close()

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")

# ----------------------------------------------------------------------
# GET_DEPOSIT_HISTORY
#
#       def get_deposit_history(self, **params):
#        """Fetch deposit history.
#
#        :param asset: optional
#        :type asset: str
#        :type status: 0(0:pending,1:success) optional
#        :type status: int
#        :param startTime: optional
#        :type startTime: long
#        :param endTime: optional
#        :type endTime: long
#        :param recvWindow: the number of milliseconds the request is valid for
#        :type recvWindow: int
#
#        :returns: API response
#
#        .. code-block:: python
#
#            {
#                "depositList": [
#                    {
#                        "insertTime": 1508198532000,
#                        "amount": 0.04670582,
#                        "asset": "ETH",
#                        "status": 1
#                    }
#                ],
#                "success": true
#            }
#
def GET_DEPOSIT_HISTORY(LOG,out_file):

	LOG.write("GET_DEPOSIT_HISTORY() " + TimeStamp() + "\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	try:
		data = client.get_deposit_history()

		S = json.dumps(data)
		json_file = out_file + ".json"
		TMP = open(json_file,'w')
		TMP.write(S)
		TMP.close()
		
		F = open(out_file,'w')
		F.write("asset\tamount\tstatus\tinsertTime\tTS\n")
		
		if data:
			for T in data['depositList']:
				TS = TimeStampUnixDateTime(T['insertTime'])
				S = '%s\t%s\t%s\t%s\t%s\n' % (T['asset'],T['amount'],T['status'],T['insertTime'],TS)
				F.write(S)
		F.close()

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")

# ----------------------------------------------------------------------
# GET_WITHDRAW_HISTORY
#
#      def get_withdraw_history(self, **params):
#        """Fetch withdraw history.
#
#        :param asset: optional
#        :type asset: str
#        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
#        :type status: int
#        :param startTime: optional
#        :type startTime: long
#        :param endTime: optional
#        :type endTime: long
#        :param recvWindow: the number of milliseconds the request is valid for
#        :type recvWindow: int
#
#        :returns: API response
#
#       .. code-block:: python
#
#            {
#                "withdrawList": [
#                    {
#                        "amount": 1,
#                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
#                        "asset": "ETH",
#                        "applyTime": 1508198532000
#                        "status": 4
#                    },
#                    {
#                        "amount": 0.005,
#                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
#                        "txId": "0x80aaabed54bdab3f6de5868f89929a2371ad21d666f20f7393d1a3389fad95a1",
#                        "asset": "ETH",
#                        "applyTime": 1508198532000,
#                        "status": 4
#                    }
#                ],

def GET_WITHDRAW_HISTORY(LOG,out_file):

	LOG.write("GET_WITHDRAW_HISTORY() " + TimeStamp() + "\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	try:
		data = client.get_withdraw_history()

		S = json.dumps(data)
		json_file = out_file + ".json"
		TMP = open(json_file,'w')
		TMP.write(S)
		TMP.close()

		F = open(out_file,'w')
		F.write("asset\tamount\tstatus\tapplyTime\tTS\taddress\ttxId\n")
		
		if data:
			for T in data['withdrawList']:
				TS = TimeStampUnixDateTime(T['applyTime'])
				S = '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (T['asset'],T['amount'],T['status'],T['applyTime'],TS,T['address'],T['txId'])
				F.write(S)
		F.close()

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")

#
# GET_EXCHANGE_INFO
#
#   .. code-block:: python

#            {
#                "timezone": "UTC",
#                "serverTime": 1508631584636,
#                "rateLimits": [
#                    {
#                        "rateLimitType": "REQUESTS",
#                        "interval": "MINUTE",
#                        "limit": 1200
#                    },
#                    {
#                        "rateLimitType": "ORDERS",
#                        "interval": "SECOND",
#                        "limit": 10
#                    },
#                    {
#                        "rateLimitType": "ORDERS",
#                        "interval": "DAY",
#                        "limit": 100000
#                    }
#                ],
#                "exchangeFilters": [],
#                "symbols": [
#                    {
#                        "symbol": "ETHBTC",
#                        "status": "TRADING",
#                        "baseAsset": "ETH",
#                        "baseAssetPrecision": 8,
#                        "quoteAsset": "BTC",
#                        "quotePrecision": 8,
#                        "orderTypes": ["LIMIT", "MARKET"],
#                        "icebergAllowed": false,
#                        "filters": [
#                            {
#                                "filterType": "PRICE_FILTER",
#                                "minPrice": "0.00000100",
#                                "maxPrice": "100000.00000000",
#                                "tickSize": "0.00000100"
#                            }, {
#                                "filterType": "LOT_SIZE",
#                                "minQty": "0.00100000",
#                                "maxQty": "100000.00000000",
#                                "stepSize": "0.00100000"
#                            }, {
#                                "filterType": "MIN_NOTIONAL",
#                                "minNotional": "0.00100000"
#
def GET_EXCHANGE_INFO(LOG,json_file,acc_file,stk_file):

	LOG.write("GET_EXCHANGE_INFO() " + TimeStamp() + "\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
	
	try:
		data = client.get_exchange_info()

		S = json.dumps(data)
		TMP = open(json_file,'w')
		TMP.write(S)
		TMP.close()

		if data:
			ACC = open(acc_file,'w')
			for rate in data['rateLimits']:
				S = "%s\t%s\t%s\n" % (rate['rateLimitType'],rate['interval'],rate['limit'])
				ACC.write(S)
			ACC.close()

			STK = open(stk_file,'w')
			S = "Symbol\tMinPrc\tLotSize\tTickSize\n"
			STK.write(S)
			for stk in data['symbols']:
				if (stk['quoteAsset'] != "BTC"):
					continue
				sym = stk['baseAsset']
				min_prc = 0.0
				lot_size = 0.0
				tick_size = 0.0
				for stk_filter in stk['filters']:
					if (stk_filter['filterType'] == 'PRICE_FILTER'):
						min_prc = stk_filter['minPrice']
						tick_size = stk_filter['tickSize']
					elif (stk_filter['filterType'] == 'LOT_SIZE'):
						lot_size = stk_filter['minQty']
				S = "%s\t%s\t%s\t%s\n" % (sym,min_prc,lot_size,tick_size)
				STK.write(S)
			STK.close()
							
	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")

#
# GET_TICKERS
#
#

#  get_all_tickers()
#
#        [
#                {
#                    "symbol": "LTCBTC",
#                    "price": "4.00000200"
#                },
#                {
#                    "symbol": "ETHBTC",
#                    "price": "0.07946600"
#                }
#            ]
#  get_orderbook_tickers()
#
#            [
#                {
#                    "symbol": "LTCBTC",
#                    "bidPrice": "4.00000000",
#                    "bidQty": "431.00000000",
#                    "askPrice": "4.00000200",
#                    "askQty": "9.00000000"
#                },
#                {
#                    "symbol": "ETHBTC",
#                    "bidPrice": "0.07946700",
#                    "bidQty": "9.00000000",
#                    "askPrice": "100000.00000000",
#                    "askQty": "1000.00000000"
#                }
#            ]
def GET_TICKERS(LOG,out_file):

	TS = TimeStamp()
	
	LOG.write("GET_TICKERS() " + TS + "\n")

	if (os.path.exists(out_file)):
		os.remove(out_file)

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")

	# Open out file
	F = open(out_file,'w')
	F.write("Symbol\tLast\tBid\tAsk\tTimestamp\n")
	LAST = {}

	# Get last prices
	#try:
	#	data = client.get_all_tickers()
	#	S = pprint.pformat(data)
	#	TMP = open('data.out','w')
	#	TMP.write(S)
	#	TMP.close()

	#	if data:
	#		for X in data:
	#			if (len(X['symbol']) == 6):
	#				A = X['symbol'][0:3]
	#				B = X['symbol'][3:6]
	#			elif (len(X['symbol']) == 7):
	#				A = X['symbol'][0:3]
	#				B = X['symbol'][3:7]
	#				if (A == "BTC" and B == "USDT"):
	#					B = "BTC"
	#				else:
	#					A = X['symbol'][0:4]
	#					B = X['symbol'][4:7]
	#			elif (len(X['symbol']) == 8):
	#				A = X['symbol'][0:5]
	#				B = X['symbol'][5:8]
	#			elif (len(X['symbol']) == 5):
	#				A = X['symbol'][0:2]
	#				B = X['symbol'][2:5]
	#			if (B != "BTC"):
	#				continue
	#			LAST[A] = X['price']
			
	#except BinanceAPIException as e:
	#	print(e.status_code)
	#	print(e.message)
	#	LOG.write(e.message + "\n")

	# Get bid/ask and output to file
	try:
	
		data = client.get_orderbook_tickers()

		TS = TimeStampShort()
		
		#S = pprint.pformat(data)
		#TMP = open('data.out','w')
		#TMP.write(S)
		#TMP.close()
		
		if data:
			for X in data:
				if (len(X['symbol']) == 6):
					A = X['symbol'][0:3]
					B = X['symbol'][3:6]
				elif (len(X['symbol']) == 7):
					A = X['symbol'][0:3]
					B = X['symbol'][3:7]
					if (A == "BTC" and B == "USDT"):
						B = "BTC"
					else:
						A = X['symbol'][0:4]
						B = X['symbol'][4:7]
				elif (len(X['symbol']) == 8):
					A = X['symbol'][0:5]
					B = X['symbol'][5:8]
				elif (len(X['symbol']) == 5):
					A = X['symbol'][0:2]
					B = X['symbol'][2:5]
				if (A == "BTC" and B == "USDT"):
					B = "BTC"
				if (B != "BTC"):
					continue
				prc = (float(X['bidPrice']) + float(X['askPrice'])) / 2.0
				#S = "%s\t%s\t%s\t%s\t%s" % (A,LAST[A],X['bidPrice'],X['askPrice'],TS)
				S = "%s\t%s\t%s\t%s\t%s" % (A,prc,X['bidPrice'],X['askPrice'],TS)
				F.write(S)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")

	F.close()
		
#
# GET_POSITIONS
#
#   Call:     get_account()
# 
def GET_POSITIONS(LOG,pos_file):

	TS = TimeStamp()

	LOG.write("GET_POSITIONS() " + TS + "\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	try:
		data = client.get_account()

		S = json.dumps(data)
		json_file = pos_file + ".json"
		TMP = open(json_file,'w')
		TMP.write(S)
		TMP.close()

		# Positions
		F2 = open(pos_file,'w')
		for bal in data['balances']:
			if (float(bal['free']) < .000000001):
				continue
			S = '%s\t%.8f\n' % (bal['asset'],float(bal['free']))
			F2.write(S)
		F2.close()

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
		LOG.write(e.message + "\n")
		
#
# GET_TRADES
#
#    def get_my_trades(self, **params):
#        """Get trades for a specific symbol.

#        https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-trade-list-user_data

#        :param symbol: required
#        :type symbol: str
#        :param limit: Default 500; max 500.
#        :type limit: int
#        :param fromId: TradeId to fetch from. Default gets most recent trades.
#        :type fromId: int
#        :param recvWindow: the number of milliseconds the request is valid for
#        :type recvWindow: int

#        :returns: API response

#        .. code-block:: python
#
#            [
#                {
#                    "id": 28457,
#                    "price": "4.00000100",
#                    "qty": "12.00000000",
#                    "commission": "10.10000000",
#                    "commissionAsset": "BNB",
#                    "time": 1499865549590,
#                    "isBuyer": true,
#                    "isMaker": false,
#                    "isBestMatch": true
#                }
#            ]
#       :raises: BinanceResponseException, BinanceAPIException
#
def GET_TRADES(LOG,univ,out_file):

	TS = TimeStamp()

	LOG.write("GET_TRADES() " + TS + "\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	DATA = []
	
	F = open(out_file,'w')
	F.write("symbol\tid\tprice\tqty\tcommission\tcommissionAsset\ttime\tTS\n")
	for u in univ:
		if (u == "BTC"):
			continue
		try:
			sym = u + "BTC"
			#print(sym)
			data = client.get_my_trades(symbol=sym)
			if data is None:
				continue
			for T in data:
				TS = TimeStampUnixDateTime(T['time'])
				S = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %    \
				    (u,T['id'],T['price'],T['qty'], \
				       T['commission'],T['commissionAsset'],T['time'],TS)
				F.write(S)
			DATA.append(data)

		except BinanceAPIException as e:
			print(e.status_code)
			print(e.message)
			LOG.write(e.message + "\n")

	F.close()

	S = json.dumps(DATA)
	json_file = out_file + ".json"
	TMP = open(json_file,'w')
	TMP.write(S)
	TMP.close()


#
# GET_ALL_ORDERS
#
#       def get_all_orders(self, **params):
#
#       """Get all account orders; active, canceled, or filled.
#
#        :param symbol: required
#        :type symbol: str
#        :param orderId: The unique order id
#        :type orderId: int
#        :param limit: Default 500; max 500.
#        :type limit: int
#        :param recvWindow: the number of milliseconds the request is valid for
#        :type recvWindow: int
#        :returns: API response
#        .. code-block:: python
#            [
#                {
#                    "symbol": "LTCBTC",
#                    "orderId": 1,
#                    "clientOrderId": "myOrder1",
#                    "price": "0.1",
#                    "origQty": "1.0",
#                    "executedQty": "0.0",
#                    "status": "NEW",
#                    "timeInForce": "GTC",
#                    "type": "LIMIT",
#                    "side": "BUY",
#                    "stopPrice": "0.0",
#                    "icebergQty": "0.0",
#                    "time": 1499827319559
#                }
def GET_ALL_ORDERS(LOG,univ,out_file):

	LOG.write(TimeStamp() + "GET_ALL_ORDERS\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	F = open(out_file,'w')
	F.write("symbol\torderId\tclientOrderId\tprice\torigQty\texecutedQty\tstatus\ttimeInForce\ttype\tside\tstopPrice\ticebergQty\ttime\tTS\n")
	for u in univ:
		if (u == "BTC"):
			continue
		try:
			sym = u + "BTC"
			#print(sym)
			data = client.get_all_orders(symbol=sym)
			if data is None:
				continue
			for T in data:
				TS = TimeStampUnixDateTime(T['time'])
				S = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %    \
				    (u,T['orderId'],T['clientOrderId'],T['price'],T['origQty'], \
				       T['executedQty'],T['status'],T['timeInForce'],T['type'], \
				       T['side'],T['stopPrice'],T['icebergQty'],T['time'],TS)
				F.write(S)

		except BinanceAPIException as e:
			print(e.status_code)
			print(e.message)
			LOG.write(e.message + "\n")

	F.close()

# ----------------------------------------------------------------------
# GET_OPEN_ORDERS
#
#        def get_open_orders(self, **params):
#
#        """Get all open orders on a symbol.
#
#        :param symbol: optional
#        :type symbol: str
#        :param recvWindow: the number of milliseconds the request is valid for
#        :type recvWindow: int
#
#        :returns: API response
#
#        .. code-block:: python
#
#            [
#                {
#                    "symbol": "LTCBTC",
#                    "orderId": 1,
#                    "clientOrderId": "myOrder1",
#                    "price": "0.1",
#                    "origQty": "1.0",
#                    "executedQty": "0.0",
#                    "status": "NEW",
#                    "timeInForce": "GTC",
#                    "type": "LIMIT",
#                    "side": "BUY",
#                    "stopPrice": "0.0",
#                    "icebergQty": "0.0",
#                    "time": 1499827319559
#                }
#           ]
def GET_OPEN_ORDERS(LOG,univ,out_file):

	LOG.write(TimeStamp() + "GET_OPEN_ORDERS\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	DATA = []
	F = open(out_file,'w')
	F.write("symbol\torderId\tclientOrderId\tprice\torigQty\texecutedQty\tstatus\ttimeInForce\ttype\tside\tstopPrice\ticebergQty\ttime\tTS\n")
	for u in univ:
		if (u == "BTC"):
			continue
		try:
			sym = u + "BTC"
			#print(sym)
			data = client.get_open_orders(symbol=sym)
			if data is None:
				continue
			for T in data:
				TS = TimeStampUnixDateTime(T['time'])
				S = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %    \
				    (u,T['orderId'],T['clientOrderId'],T['price'],T['origQty'], \
				       T['executedQty'],T['status'],T['timeInForce'],T['type'], \
				       T['side'],T['stopPrice'],T['icebergQty'],T['time'],TS)
				F.write(S)
			DATA.append(data)
			
		except BinanceAPIException as e:
			print(e.status_code)
			print(e.message)
			LOG.write(e.message + "\n")

	F.close()
	return DATA

# ----------------------------------------------------------------------
# CANCEL_OPEN_ORDERS
#
#        def get_open_orders(self, **params):
#
#        """Get all open orders on a symbol.
#
#        :param symbol: optional
#        :type symbol: str
#        :param recvWindow: the number of milliseconds the request is valid for
#        :type recvWindow: int
#
#        :returns: API response
#
#        .. code-block:: python
#
#            [
#                {
#                    "symbol": "LTCBTC",
#                    "orderId": 1,
#                    "clientOrderId": "myOrder1",
#                    "price": "0.1",
#                    "origQty": "1.0",
#                    "executedQty": "0.0",
#                    "status": "NEW",
#                    "timeInForce": "GTC",
#                    "type": "LIMIT",
#                    "side": "BUY",
#                    "stopPrice": "0.0",
#                    "icebergQty": "0.0",
#                    "time": 1499827319559
#                }
#           ]
#       def cancel_order(self, **params):
#
#       """Cancel an active order. Either orderId or origClientOrderId must be sent.
#
#        :param symbol: required
#        :type symbol: str
#        :param orderId: The unique order id
#        :type orderId: int
#        :param origClientOrderId: optional
#        :type origClientOrderId: str
#        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
#        :type newClientOrderId: str
#        :param recvWindow: the number of milliseconds the request is valid for
#        :type recvWindow: int
#
#        :returns: API response
#
#        .. code-block:: python
#
#            {
#                "symbol": "LTCBTC",
#                "origClientOrderId": "myOrder1",
#                "orderId": 1,
#                "clientOrderId": "cancelMyOrder1"
#            }
def CANCEL_OPEN_ORDERS(LOG,univ,out_file):

	LOG.write(TimeStamp() + "CANCEL_OPEN_ORDERS\n")

	try:
		client = Client(api_key, api_secret)

	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)

	F = open(out_file,'w')
	F.write(TimeStamp() + "\n")
	for u in univ:
		if (u == "BTC"):
			continue
		try:
			sym = u + "BTC"
			#print(sym)
			data = client.get_open_orders(symbol=sym)
			if data is None:
				continue
			for T in data:
				TS = TimeStampUnixDateTime(T['time'])
				S = 'Order:\n'
				F.write(S)
				S = '\tSymbol:   \t%s\t%s\n' % (u,sym)
				F.write(S)
				S = '\tQty:      \t%s\n' % (T['origQty'])
				F.write(S)
				S = '\tPrice:    \t%s\n' % (T['price'])
				F.write(S)
				S = '\tOrder Id: \t%s\n\n' % (T['orderId'])
				F.write(S)

				try:
					RV = client.cancel_order(symbol=sym,orderId=T['orderId'])
					if (RV):
						S = 'Return Value:\n'
						F.write(S)
						S = '\tSymbol:              \t%s\n' % (RV['symbol'])
						F.write(S)
						S = '\torigClientOrderId:	\t%s\n' % (RV['origClientOrderId'])
						F.write(S)
						S = '\torderId:	            \t%s\n' % (RV['orderId'])
						F.write(S)
						S = '\tclientOrderId:	    \t%s\n\n\n' % (RV['clientOrderId'])
						F.write(S)
				
				except BinanceAPIException as e:
					print(e.status_code)
					print(e.message)
					LOG.write(e.message + "\n")

		except BinanceAPIException as e:
			print(e.status_code)
			print(e.message)
			LOG.write(e.message + "\n")

	F.close()
