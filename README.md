# Stockli

Api, które korzysta z innych api do szybkiego przeliczenia walut w terminalu. 

## Skrypt
Do działania skryptu wymagany jest python, a także pyqt6
```bash
pip install pyqt6
```
Po zainstalowaniu skrypt wywołujemy tradycyjnie:
```bash
python stockcli.py [parametry]
```
### Dostępne parametry
- **-h**:  wyświetla pomoc w terminalu
- **-l**: wyświela link do listy dostępnych waluty
- **-f**: w połączeniu z parametrem **-l** wyświetla listę w terminalu
- **-c**: konwertuje podane waluty. Przyjmuje argumenty: wartość, waluta z której przeliczamy, waluta do której przeliczamy
- **-a**: deklaruje dokładność z jaką waluty mają być przeliczone
- **-g**: tryb graficzny
- **-d**: działa tylko w trybie pośrednim. Nieobowiązkowy. Wykonuje przeliczenie w trybie bezpośrednim. Nie działa w trybie graficznym.
- **-p**: działa tylko w trybie bezpośrednim. Nieobowiązkowy. Wykonuje przeliczenie w trybie pośrednim. Nie działa w trybie graficznym.
### Przykładowe użycie

```bash
python stockcli.py -c 50 PLN EUR -a 2
50 PLN -> 11.62 EUR
```
Parametr -a nie jest obowiązkowy.

### Tryb bezpośredni
Skrypt jest w stanie pominąć pośredni serwer i samodzielnie przeliczyć waluty. W takim wypadku wymagane jest aby podać własne klucze do serwisów wypisanych poniżej. Aby używać trybu bezpośredniego należy dodać parametr -d. Możemy również ustawić go jako  domyślny. Aby to zrobić należy edytować skrypt:
```python
direct_default = False #indirect by default
url = "" #indirect server url
api_fiat = "" #openexchangerates api key
api_crypto = "" #coingecko api key
```
W tym miejscu należy podać także własne klucze.

## Api
Napisane we flasku, w pythonie. W przypadku samodzielnego hostingu należy pamiętać, aby edytować adresy w kodzie, a także dodać własne klucze. Wymaga do działania ściągniętych wcześniej danych. Przy pierwszym uruchomienu należy ściągnąć ręcznie pliki, bądź użyć funkcji init:
```python
from getstock import stockManager
stockManager.init()
```
Funkcja ściąga pliki potrzebne do dalszego działania programu do folderu data.

## Użyte serwisy
- https://coingecko.com
- https://openexchangerates.org
