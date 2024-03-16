import argparse
from PyQt6.QtWidgets import QApplication, QWidget, QDoubleSpinBox, QComboBox, QPushButton
import requests
import json

url = "http://127.0.0.1:5000/cli" #! page url

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
        default="N",
        nargs=1,
        help="ACCURACY - specify convert accuracy in number of digits"
    )
    parser.add_argument(
        '-g',
        action="store_true",
        help="GUI - start the gui"
    )
    return parser.parse_args()

def gui():
    def submit():
        value = line_first.value()
        fromm = box_first.currentText()
        to = box_second.currentText()
        occur = line_first.decimals()
        myobj = {"start" : fromm, "value" : value, "end" : to, "accur" : occur}
        response = requests.get(url+"/cli", myobj)
        line_second.setValue(float(response.text))

    def accuracy(accur):
        line_first.setDecimals(accur)
        line_second.setDecimals(accur)
        line_first.setSingleStep(1 * (10 ** -accur))
        line_second.setSingleStep(1 * (10 ** -accur))

    currmap = json.loads(requests.get(url+"/list").text)
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
    if params.f == False:
        print(f"you can see the json list at : {url}/list \nadd parameter -f to print it here")
    else:
        response = requests.get(url+"/list")
        print(response.text)
else:
    if not params.c == None:
        if params.a == None:
            myobj = {"start" : params.c[1], "value" : params.c[0], "end" : params.c[2], "accur" : params.a[0]}
            response = requests.get(url+"/cli", myobj)
        else:
            myobj = {"start" : params.c[1], "value" : params.c[0], "end" : params.c[2]}
            response = requests.get(url+"/cli", myobj)
        print(f'{params.c[0]} {params.c[1]} -> {response.text} {params.c[2]}')