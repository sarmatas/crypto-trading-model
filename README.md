# crypto-trading-model

Project Overiew

Goals

  Implement a complete cryptocurrency trading framework. Including continuously updated database, quantitative research tools,
  backtesting and simulation platform, real-time monitoring, p&l reporting and a working equity portfolio style statistical 
  arbitrage model.
  
Note

  These are representative programs only, not the entire infrastructure.
  
  CryptoModel.py is the working code from a version that was traded live on the Binance exchange for 9 months.
  
  Feel free to use as desired, but this is a simple test version and is not intended to be a profitable working model. Also,
  please be aware of the substantial risks that are involved in trading on the currently available cryptocurrency exchanges and
  that these risks are much greater, and very different, than the risks involved in holding cryptocurrencies in a private wallet
  that you control.
  
  Programs
  
    Binance.py
      Wrapper to access the Binance API functions in BinanceLib.py. Intended for command line or cron.
      Provides access to all account information, balances, trade history, open orders, etc. Not intended for live trading, but
      does include a function call to cancel all outstanding orders.
      
    BinanceGetPrices.py
      Gets live prices from Binance API.
      
    BinanceLib.py
      Wrapper around    https://github.com/sammchardy/python-binance
      Also some utility functions, timestamps, round lots, etc.
      
    BitcoinCharts.py
      Various exchange related data from bitcoincharts API.
      
    CoinCapAPI.py
      Gets data from coincap.io/front and parsee out fields for each coin.
      
    CoinMarketCapTicker.py
      Access coinmarketcap.com API for list of tickers.
      
    CryptoModel.py
      Implementation of equity style, portfolioi based statistical arbitrage model in cryptocurrency space.
      This version is a simple continuously rebalanced long book which woulc be expected to capture volatility through
      market mean reversion.
      
