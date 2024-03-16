from flask import Flask, request, render_template
from getstock import stockManager
import time

app = Flask(__name__)

@app.before_request
def update():
    fiat = stockManager.loadJson("data/fiat.json")
    crypto = stockManager.loadJson("data/crypto.json")
    limits = stockManager.loadJson("data/usage.json")
 
    if time.time() - fiat["updated"] > 1800: #30 minutes delay
        if limits["openexchange"] < 1000:
            fiat = stockManager.updateFiat()
        stockManager.saveJson(fiat, "data/fiat.json")
        if time.localtime(time.time()).tm_mon != time.localtime(fiat["updated"]).tm_mon:
            limits["openexchange"] = 0
        limits["openexchange"] += 1
        limits["time"] = time.time()
        stockManager.saveJson(limits, "data/usage.json")

    if time.time() - crypto["updated"] > 300: #5 minutes delay
        if limits["coingecko"] < 10000:
            crypto = stockManager.updateCrypto()
        stockManager.saveJson(crypto, "data/cryptoFull.json")
        crypto = stockManager.simplifyCrypto("data/cryptoFull.json")
        stockManager.saveJson(crypto, "data/crypto.json")
        if time.localtime(time.time()).tm_mon != time.localtime(crypto["updated"]).tm_mon:
            limits["coingecko"] = 0
        limits["coingecko"] += 1
        limits["time"] = time.time()
        stockManager.saveJson(limits, "data/usage.json")
    
@app.route('/cli/cli', methods=['GET'])
def handle_get():
    try:
        start = request.args.get('start')
        value = request.args.get('value')
        end = request.args.get('end')
        accur = request.args.get('accur')
        pretty = request.args.get('pretty')
        if start == None or value == None or end == None:
            return "Nie można przetworzyć żądania, nie wszystkie parametry zostały podane."

        fiat = stockManager.loadJson("data/fiat.json")
        crypto = stockManager.loadJson("data/crypto.json")
        merged = fiat["rates"] | crypto
        usd = float(value) * 1/merged[start]

        if not pretty == None:
            prefix = f'{value} {start} -> '
            suffix = f' {end}'
        else:
            prefix = ""
            suffix = ""

        if not accur == None:
            return f'{prefix}{round(usd * merged[end], int(accur)):.{int(accur)}f}{suffix}'
        elif start in crypto.keys() or end in crypto.keys():
            return f'{prefix}{round(usd * merged[end],8):.8f}{suffix}'
        else: 
            return f'{prefix}{round(usd * merged[end],2)}{suffix}'
    except:
        return "Nieznany błąd :c"

@app.route('/cli')
def info():
    usage = stockManager.loadJson("data/usage.json")
    return render_template("help.html", fiatl=usage["openexchange"], cryptol=usage["coingecko"])
    
@app.route('/cli/list')
def list():
    fiat = stockManager.loadJson("data/fiat.json")
    crypto = stockManager.loadJson("data/crypto.json")
    merged = fiat["rates"] | crypto
    return merged

def get_time():
    update = stockManager.loadJson("data/fiat.json")
    timer = update["updated"]
    now = time.localtime(timer)
    hour = now.tm_hour
    return hour

@app.route('/')
def home():
    return render_template("fronted.html", timer=f"{get_time()}:00")

if __name__ == '__main__':
    if not stockManager.checkApi():
        print("Nie podano kluczy api")
        exit(0)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
    app.run(host="0.0.0.0")