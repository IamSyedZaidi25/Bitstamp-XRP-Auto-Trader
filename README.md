# btc
Core Files:
 - exchange.py
 - pickler.py
 - tick.py
 
 Other Files:
 - lol.pickle	(*.gitignored)
 - addr.pickle  (*.gitignored)
 - .gitinore
 - README.md
  
  How to pickle:
	- To pickle your keys, add them to pickler.py file:
	
			lol_k = [["BITFINEX","",""],
				["BITSTAMP","",""],
				["BTC-e","",""],
				["KRAKEN","",""],
				["GDAX","",""]]


			addr_k = { "bitfinex":{"ltcusd":"", "btcusd":""}, "bitstamp":{"ltcusd":"", "btcusd":""}}
			
			
	After they have been added to the file, save and run the pickler.py. This will create the lol.pickle and addr.pickle.
	DONT FORGET! After the pickled files have been created, go back and delete them from the pickler.py so they do not get
	commited with your keys in them.
	
	
	
	- After successful pickling of keys, you should have addr.pickle and lol.pickle in your project folder.
		These files are automatically loaded into exchange.py so no implimentation is needed.