import requests
import json
import time

class Manager:
    #Define your api keys
    api_fiat = "" #openexchangerates api key
    api_crypto = "" #coingecko api key

    def checkApi(self):
        if self.api_crypto == "" or self.api_fiat == "":
            return False
        return True

    #1000 req / month
    def updateFiat(self):
        base = "USD" #changing base is not allowed in free tier
        prettyprint = "false"
        show_alternative = "false"
        url = "https://openexchangerates.org/api/latest.json?app_id="+self.api_fiat+"&base="+base+"&prettyprint="+prettyprint+"&show_alternative="+show_alternative
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        return (json.loads(response.text) | {"updated" : int(time.time())})
    
    #10000 req / month, 30 req / minute, 60 secs freshness
    def updateCrypto(self):
        base = "USD"
        numberof = "100"
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency="+base+"&order=market_cap_desc&per_page="+numberof+"&page=1"
        headers = {"x-cg-demo-api-key": self.api_crypto}
        response = requests.get(url, headers=headers)
        return json.loads(response.text)
    
    def simplifyCrypto(self, path):
        with open(path, "r") as file:
            fullcrypto = json.load(file)
            simplycrypto = {}
            for i in range(100):
                simplycrypto.update({fullcrypto[i]["symbol"] : 1/fullcrypto[i]["current_price"]})
            simplycrypto.update({"updated" : int(time.time())})
        return simplycrypto
    
    def saveJson(self,data, path):
        with open(path,"w") as file:
            file.write(json.dumps(data, sort_keys=True, indent=4))

    def loadJson(self,path):
        with open(path,"r") as file:
            fiatmap = json.load(file)
        return fiatmap
    
    def init(self):
        self.saveJson(self.updateFiat(), "data/fiat.json")
        self.saveJson(self.updateCrypto(), "data/cryptoFull.json")
        usage = {"coingecko":0, "openexchange":0,"time":time.time()}
        self.saveJson(usage, "data/usage.json")

stockManager = Manager()