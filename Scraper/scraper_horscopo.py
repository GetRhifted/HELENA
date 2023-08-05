import datetime
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Variables de trabajo.

# URL a usar.
url = 'https://www.clarin.com/horoscopo/'

# Encapsulamos la url en un request.
horos = requests.get(url)


# Procedemos a volverlo una Soup
s_horos = BeautifulSoup(horos.text, 'lxml')

# Traemos la informacion de los signos.
signos = s_horos.find_all('div', attrs={'class':'col-lg-2 col-md-2 col-sm-6 col-xs-6'})

# Ubicamos cada signo por separado.
signo = signos[3]

# Tomamos el link de cada signo.
links_signos = [signo.a.get('href') for signo in signos]
links_full = 'https://www.clarin.com/horoscopo/' + signo.a.get('href')

# Seleccionamos el link que queremos usar y 
link_select = requests.get(links_full)



