import json
import hashlib
import hmac
import time
import requests
import base64
import pickle
import tick
import smtplib
import cherrypy
import os, os.path
lol_file = open("lol.pickle", "rb")
lol = pickle.load(lol_file)
lol_file.close()
addr_file = open("addr.pickle","rb")
addr = pickle.load(addr_file)
addr_file.close()
global_vars = open("globals.pickle","rb")
global_v = pickle.load(global_vars)
global_vars.close()
sendMessg = open("sendMessg.pickle","rb")
sendLoc = pickle.load(sendMessg)
sendMessg.close()

lbalance = {}




def emailIt(message):
    loc = sendLoc[0]
    message = message
    pw = sendLoc[1]
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(loc,pw)
    server.sendmail(loc,loc,message)
    server.quit()



def adr(exchange,curr):
    address = addr[exchange][curr]
    return address

def bitstamp(method,**kwargs):
    urlappend = {"ltcusd":"ltc_withdrawal/","btcusd":"btc_withdrawal/"}  # for transfers only
    method = method
    pNonce = str(time.time()).split('.')[0]
    nonce = pNonce
    key = lol[1][1]
    secret = lol[1][2]
    customer_id = global_v["bitstamp_cust_id"]
    message = (nonce + customer_id + key)
    sign = hmac.new(secret.encode(),message.encode(), hashlib.sha256).hexdigest().upper()


    if method == "balance":
        global lbalance
        data = ({ 'key': key,'signature':sign,'nonce':nonce})
        r = requests.post("https://www.bitstamp.net/api/v2/balance/",data)
        r = json.loads(r.text)
        r = [float(r["btc_available"]),float(r["ltc_available"]),float(r["usd_available"])]
        lbalance['BITSTAMP'] = (r[0],r[1],r[2])
        return("BITSTAMP: "+"BTC: "+str(r[0])+"   LTC: "+str(r[1])+"   USD: "+str(r[2]))

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

    if method == "transfer":
        curr = ""
        instant = 0
        amount = kwargs['amount']
        address = kwargs['address']
        data = ({ "key": key,"signature":sign,"nonce":nonce,"amount":amount,"address":address,"instant":instant})
        for dic in addr:
            for k in addr[dic]:
                for v in addr[dic][k].splitlines():

                    if address == v:
                        curr = k
        url = ""
        if curr == "btcusd":
            url = "https://www.bitstamp.net/api/bitcoin_withdrawal/"
        if curr == "ltcusd":
            url = "https://www.bitstamp.net/api/v2/ltc_withdrawal/"
        r = requests.post(url,data)
        r = json.loads(r.text)
        if r != "":
            emailIt("Subject: Exchange Program: Transfer\n\n"+str(r))
        return(r)





def bitfinex(method, **kwargs):
    method = method
    pNonce = str(time.time()).split('.')[0]
    nonce = pNonce
    key = lol[0][1]
    secret = lol[0][2]

    if method == "balance":
        global lbalance
        payload = {"request": "/v1/balances","nonce": nonce }
        sign = json.dumps(payload)
        data = base64.standard_b64encode(sign.encode('utf8'))
        sign = base64.standard_b64encode(sign.encode('utf8'))
        h = hmac.new(secret.encode('utf8'), sign, hashlib.sha384)
        sign = h.hexdigest()
        headers = {"X-BFX-APIKEY": key, "X-BFX-SIGNATURE": sign, "X-BFX-PAYLOAD": data}
        r = requests.get("https://api.bitfinex.com/v1/balances", headers = headers )
        if r.text == "[]":
            lbalance['BITFINEX'] = (r[0],r[2],r[3])
            return("BITFINEX: BTC: 0.0 LTC: 0.0 USD: 0.0")
        else:
            r = json.loads(r.text)
            lbalance['BITFINEX'] = (r[0]["available"],r[2]["available"],r[3]["available"])
            return("BITFINEX: "+"BTC: "+str(r[0]["available"])+"   LTC: "+str(r[2]["available"])+"   USD: "+str(r[3]["available"]))



    if method == "open":
        payload = {"request": "/v1/orders","nonce": nonce }
        sign = json.dumps(payload)
        data = base64.standard_b64encode(sign.encode('utf8'))
        sign = base64.standard_b64encode(sign.encode('utf8'))
        h = hmac.new(secret.encode('utf8'), sign, hashlib.sha384)
        sign = h.hexdigest()
        headers = {"X-BFX-APIKEY": key, "X-BFX-SIGNATURE": sign, "X-BFX-PAYLOAD": data}
        r = requests.get("https://api.bitfinex.com/v1/orders", headers = headers )
        r = json.loads(r.text)
        return(r)

    if method == "buy":
        cp = kwargs['cp']
        amount = kwargs['amount']
        payload = {"request": "/v1/order/new","nonce": nonce,"side":"buy","type":"exchange market","amount":amount,"symbol":cp,"price":"0.1" }
        sign = json.dumps(payload)
        data = base64.standard_b64encode(sign.encode('utf8'))
        sign = base64.standard_b64encode(sign.encode('utf8'))
        h = hmac.new(secret.encode('utf8'), sign, hashlib.sha384)
        sign = h.hexdigest()
        headers = {"X-BFX-APIKEY": key, "X-BFX-SIGNATURE": sign, "X-BFX-PAYLOAD": data}
        r = requests.post("https://api.bitfinex.com/v1/order/new/", headers = headers )
        r = json.loads(r.text)
        if r != "":
            emailIt("Subject: Exchange Program: Buy\n\n"+str(r))
        return(r)

    if method == "sell":
        cp = kwargs['cp']
        amount = kwargs['amount']
        payload = {"request": "/v1/order/new","nonce": nonce, "side":"sell","type":"exchange market","amount":amount,"symbol" : cp ,"price":"0.1"}
        sign = json.dumps(payload)
        data = base64.standard_b64encode(sign.encode('utf8'))
        sign = base64.standard_b64encode(sign.encode('utf8'))
        h = hmac.new(secret.encode('utf8'), sign, hashlib.sha384)
        sign = h.hexdigest()
        headers = {"X-BFX-APIKEY": key, "X-BFX-SIGNATURE": sign, "X-BFX-PAYLOAD": data}
        r = requests.post("https://api.bitfinex.com/v1/order/new/", headers = headers )
        r = json.loads(r.text)


        if r != "":
            emailIt("Subject: Exchange Program: Sell\n\n"+str(r))
        return(r)

    if method == "transfer":
        amount = kwargs['amount']
        address = kwargs['address']

        payload = {"request": "/v1/withdraw","nonce": nonce,"withdraw_type":"litecoin","walletselected":"exchange","amount":amount, "address":address }
        sign = json.dumps(payload)
        data = base64.standard_b64encode(sign.encode('utf8'))
        sign = base64.standard_b64encode(sign.encode('utf8'))
        h = hmac.new(secret.encode('utf8'), sign, hashlib.sha384)
        sign = h.hexdigest()
        headers = {"X-BFX-APIKEY": key, "X-BFX-SIGNATURE": sign, "X-BFX-PAYLOAD": data}
        r = requests.post("https://api.bitfinex.com/v1/withdraw/", headers = headers )
        r = json.loads(r.text)
        if r != "":
            emailIt("Subject: Exchange Program: Transfer\n\n"+str(r))

        return(r)



    print(bitfinex("balance"))
