import argparse
from PyQt6.QtWidgets import QApplication, QWidget, QDoubleSpinBox, QComboBox, QPushButton
import requests
import json

direct_default = False #indirect by default
url = "https://stockcli.kackrol.ovh/cli" #indirect server url
api_fiat = "" #openexchangerates api key
api_crypto = "" #coingecko api key

def parser():
    parser = argparse.ArgumentParser(
    description="A simple script for stockcli to convert $$$",
    epilog="Remember to use currencies alias in <from> and <to> e.g USD, EUR, BTC. See list if in trouble.")
    parser.add_argument(
        '-l',
        action="store_true",
        help="LIST - display list of currencies"
    )
    parser.add_argument(
        '-f',
        action="store_true",
        help="FORCE - force to print a list in terminal"
    )
    parser.add_argument(
        '-c',
        action="extend",
        metavar=("<value>", "<from>", "<to>"),
        nargs=3,
        help="CONVERT - quickly convert currencies aliases"
    )
    parser.add_argument(
        '-a',
        action='store',
        metavar="<digits>",
        nargs=1,
        help="ACCURACY - specify convert accuracy in number of digits"
    )
    parser.add_argument(
        '-g',
        action="store_true",
        help="GUI - start the gui"
    )
    if direct_default:
        parser.add_argument(
            '-p',
            action="store_true",
            help="PEER - use script with server url as a peer"
        )
    else:
        parser.add_argument(
            '-d',
            action="store_true",
            help="DIRECT - use script with your own api keys, without any peers"
        )
    return parser.parse_args()

def fetch():
    url = "https://openexchangerates.org/api/latest.json?app_id="+api_fiat
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    fiat = json.loads(response.text)
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1"
    headers = {"x-cg-demo-api-key": api_crypto}
    response = requests.get(url, headers=headers)
    crypto = json.loads(response.text)
    simplycrypto = {}
    for i in range(100):
        simplycrypto.update({crypto[i]["symbol"] : 1/crypto[i]["current_price"]})
    return fiat["rates"], simplycrypto

def direct(fiat, crypto, start,value,end,accur=None):
    merged = fiat | crypto
    usd = float(value) * 1/merged[start]
    if not accur == None:
        return f'{round(usd * merged[end], int(accur)):.{int(accur)}f}'
    elif start in crypto.keys() or end in crypto.keys():
        return f'{round(usd * merged[end],8):.8f}'
    else: 
        return f'{round(usd * merged[end],2)}'
    
def peer(start,value,end,accur=False):
    if accur:
        myobj = {"start" : start, "value" : value, "end" : end, "accur" : accur}
        response = requests.get(url+"/cli", myobj)
        return response.text
    else:
        myobj = {"start" : start, "value" : value, "end" : end}
        response = requests.get(url+"/cli", myobj)
        return response.text
    
def gui():
    def submit():
        value = line_first.value()
        fromm = box_first.currentText()
        to = box_second.currentText()
        occur = line_first.decimals()
        if direct_default:
            line_second.setValue(float(direct(fiat,crypto,fromm,value,to,occur)))
        else:
            line_second.setValue(float(peer(fromm,value,to,occur)))

    def accuracy(accur):
        line_first.setDecimals(accur)
        line_second.setDecimals(accur)
        line_first.setSingleStep(1 * (10 ** -accur))
        line_second.setSingleStep(1 * (10 ** -accur))

    fiat, crypto = fetch()
    currmap = fiat | crypto
    currlist = list(currmap.keys())

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Stockview GUI")
    window.setFixedSize(350, 250)

    line_first = QDoubleSpinBox(window)
    line_first.setGeometry(20, 20, 250, 30)
    line_first.setMaximum(99999999)
    line_first.setSingleStep(0.01)

    bplus = QPushButton("+",window)
    bplus.setGeometry(280,20,25,25)

    bminus = QPushButton("-",window)
    bminus.setGeometry(310,20,25,25)
    
    box_first = QComboBox(window)
    box_first.addItems(currlist)
    box_first.setGeometry(20, 50, 120, 30)

    line_second = QDoubleSpinBox(window)
    line_second.setGeometry(20, 100, 250, 30)
    line_second.setMaximum(99999999)
    line_second.setSingleStep(0.01)
    line_second.setReadOnly(True)

    box_second = QComboBox(window)
    box_second.addItems(currlist)
    box_second.setGeometry(20, 130, 120, 30)

    button = QPushButton("Rock and Roll", window)
    button.setGeometry(100, 180, 150, 30)

    bplus.clicked.connect(lambda: accuracy(8))
    bminus.clicked.connect(lambda: accuracy(2))
    button.clicked.connect(submit)

    window.show()
    app.exec()

params = parser()
if params.g == True:
    gui()
elif params.l == True:
    if not direct_default:
        if params.f == False:
            print(f"you can see the json list at : {url}/list \nAdd parameter -f to print it here")
        else:
            response = requests.get(url+"/list")
            print(response.text)
    else:
        if direct_default:
            if params.f == False:
                print("You cant the see list in web in direct mode\nAdd -f to print it here")
            else:
                fiat, crypto = fetch()
                merged = fiat | crypto
                print(f"{merged}")
else:
    def printDirect():
        fiat, crypto = fetch()
        if not params.c == None:
            if params.a == None:
                response = direct(fiat, crypto, params.c[1], params.c[0], params.c[2])
            else:
                response = direct(fiat, crypto, params.c[1], params.c[0], params.c[2], params.a[0])
        print(f'{params.c[0]} {params.c[1]} -> {response} {params.c[2]}')
    def printPeer():
        if not params.c == None:
            if params.a == None:
                response = peer(params.c[1], params.c[0], params.c[2])
            else:
                response = peer(params.c[1], params.c[0], params.c[2], params.a[0])
            print(f'{params.c[0]} {params.c[1]} -> {response} {params.c[2]}')

    if direct_default:
        if params.p:
            printPeer()
        else:
            printDirect()
    else:
        if params.d:
            printDirect()
        else:
            printPeer()
