import pickle

key_file = {
"BITSTAMP":["key","secret"],
"customer_id":"ENTER CUSTOMER ID HERE",
"GMAIL":["ENTER USERNAME HER","PASSWORD HERE"]
}

key = open("key.pickle","wb")
pickle.dump(key_file,key)
key.close()
