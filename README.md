# XRP Auto Trader
![alt text](https://github.com/danielreyes61/Bitcoin-Trader/blob/master/screenshot.png?raw=true)

Core Files:
 - exchange_account_access.py
 - pickler.py

 Other Files:
 - key.pickle	(*.gitignored)

 - .gitinore
 - README.md
 - LICENSE

  How to pickle:

	- To pickle your keys, add them to pickler.py file:

  key_file = {
              "BITSTAMP":["key","secret"],
              "customer_id":"ENTER CUSTOMER ID HERE",
              "GMAIL":["ENTER USERNAME HERE","PASSWORD HERE"]
              }

		This file is automatically loaded into exchange_account_access.py so no implementation is needed.
