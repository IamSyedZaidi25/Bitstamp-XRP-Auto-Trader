import json
import hashlib
import hmac
import time
import requests
import base64
import pickle
import smtplib
import os, os.path

key_file = open("key.pickle", "rb")
key_loaded = pickle.load(key_file)
key_file.close()

def emailNotify(message):
    loc = key_loaded["GMAIL"][0]
    message = message
    pw = key_loaded["GMAIL"][1]
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(loc,pw)
    server.sendmail(loc,loc,message)
    server.quit()

def bitstamp(method,**kwargs):
    method = method
    key = key_loaded["BITSTAMP"][0]
    secret = key_loaded["BITSTAMP"][1]
    customer_id = key_loaded["customer_id"]
    nonce = str(time.time()).split('.')[0]
    message = (nonce + customer_id + key)
    sign =  hmac.new(secret.encode(),
            message.encode(),
            hashlib.sha256).hexdigest().upper()
    data = ({
            'key': key,
            'signature':sign,
            'nonce':nonce
            })

    #Public Request
    x = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpusd/")
    x = json.loads(x.text)
    vwap = float(x["vwap"])
    xrp_bid =    x["bid"]
    xrp_ask =    x["ask"]
    xrp_last =   x["last"]

    #Authenticated Request
    r = requests.post("https://www.bitstamp.net/api/v2/balance/",data)
    r = json.loads(r.text)
    usd_balance = r["usd_balance"]
    xrp_balance = r["xrp_balance"]
    xrp_available = r["xrp_available"]
    nonce = str(time.time()).split('.')[0]

    #Payload
    message = (nonce + customer_id + key)
    sign = hmac.new(secret.encode(),message.encode(), hashlib.sha256).hexdigest().upper()
    data = ({ 'key': key,'signature':sign,'nonce':nonce, 'limit':1})

    m = requests.post("	https://www.bitstamp.net/api/v2/user_transactions/xrpusd/",data)

    m = json.loads(m.text)


    #Variable Extraction
    saleOrBuy       = m[0]['xrp'] #if negative, was a sell, if positive, it was a buy
    lastPriceAction = m[0]['xrp_usd'] # price of what we paid or sold for last
    fee             = m[0]['fee'] #will give fee of last transaction
    amountToBuy     = int(abs(float(m[0]['usd']))/lastPriceAction)
    fee             = float(fee) / float(amountToBuy)
    exitHardLine    = float(fee) +  lastPriceAction + (float(lastPriceAction) * 0.06)
    enterHardLine   = float(fee) + lastPriceAction - (float(lastPriceAction) * 0.06)

    #Trading Algorithm Looking for 6% gain, can be adjusted easily.
    if(float(saleOrBuy) > 0.0): # if last action was positive, it was a buy.
        if(exitHardLine < vwap):
                print("Should sell: " + str(exitHardLine))
                print("\a")
        else:
            print("Waiting to sell at: " + str(exitHardLine))

    if(float(saleOrBuy) < 0.0):
        if(enterHardLine > vwap):
            print("Should buy: " + str(enterHardLine))
            print("\a")
        else:
            print("Waiting to buy at: " + str(enterHardLine))
    else:
        print("Not a good time. Holding....")


    # Main information Dashboard
    print(
    "Total Value: $" +
    str((float(xrp_balance) * float(xrp_last)) +
    float(usd_balance)) + "\n" +
    "XRP Quantity: " + xrp_balance + "\n"
    "XRP Last: " + xrp_last + "\n"
    "XRP Bid: " + xrp_bid + "\n"
    "XRP Ask: " + xrp_ask + "\n"
    "vwap: " + str(vwap) + "\n"
    )


    # Buy and Sell supported multiple exchanges originally. Will refactor to
    # create method calls to be placed in the buy and sell algorithm.
    if method == "buy":
        cp = kwargs['cp']
        amount = kwargs['amount']
        data = ({ 'key': key,'signature':sign,'nonce':nonce,'amount':amount})
        r = requests.post("https://www.bitstamp.net/api/v2/buy/market/"+"cp"+"/",data)
        r = json.loads(r.text)
        if r != "":
            emailIt("Subject: Exchange Program: Buy\n\n"+str(r))
        return(r)

    if method == "sell":
        amount = kwargs['amount']
        cp = kwargs['cp']
        data = ({ 'key': key,'signature':sign,'nonce':nonce,'amount':amount})
        r = requests.post("https://www.bitstamp.net/api/v2/sell/market/"+cp+"/",data)
        r = json.loads(r.text)
        if r != "":
            emailIt("Subject: Exchange Program: Sell\n\n"+str(r))
        return(r)

    if method == "open":
        data = ({ 'key': key,'signature':sign,'nonce':nonce})
        r = requests.post("https://www.bitstamp.net/api/v2/open_orders/all/",data)
        r = json.loads(r.text)
        return(r)

while(1):
    try:
        print("\n" * 50)
        bitstamp("")

        time.sleep(15)
    except:
        print("\n" * 50)
        print("Network Error. Retrying...")
        time.sleep(15)
