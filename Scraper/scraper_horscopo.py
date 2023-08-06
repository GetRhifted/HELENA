import datetime
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from html import unescape

# Variables de trabajo.

# URL a usar.
url = 'https://www.hola.com/'

# Encapsulamos la url en un request.
horos = requests.get(url)


# Procedemos a volverlo una Soup
s_horos = BeautifulSoup(horos.text, 'lxml')

# Traemos las secciones de la pagina web.
secciones = s_horos.find('ul', attrs={'class':'mainSections'}).find_all('li')

# Traemos la seccion que nos interesa, en este caso el indice 47 de la lista de secciones.
seccion = secciones[47]

# Traemos los links de las secciones.
links_secciones = ['https://www.hola.com' + seccion.a.get('href') for seccion in secciones]

# Luego, elegimos el link de la seccion que vamos a usar. En este caso el indice 47.
link_trabajo = requests.get(links_secciones[47])

# Hacemos una Soup con el link que hemos seleccionado.
s_linkhoroscopos = BeautifulSoup(link_trabajo.text, 'lxml')

# Traemos una lista con los signos del zodiaco.
lista_signos = s_linkhoroscopos.find('section', attrs={'class':'col-xs-12 col-md-8'}).find_all('a')

# Tomo los links de esa lista.
links_signos = ['https://www.hola.com' + signo.get('href') for signo in lista_signos]


# Scripts de Trabajo.
try:
    def scrap_horos(s_horos):
        horos_dict = {}

        Titulo = s_horos.find('h1', attrs={'id': 'titprev'})
        if Titulo:
            horos_dict['Titulo'] = Titulo.text
        else:
            horos_dict['Titulo'] = None

        Prediccion = s_horos.find('div', attrs={'id': 'resultados'})
        if Prediccion:
            horos_dict['Prediccion'] = Prediccion.text
        else:
            horos_dict['Prediccion'] = None
        

        return horos_dict


except Exception as e:
    print('Error:')
    print(e)
    print('\n')

# Segundo Script.
def scrape_prediccion(url):
    try:
        prediccion = requests.get(url)
    except Exception as e:
        print('Error scrapeando URL', url)
        print(e)
        return None
    
    if prediccion.status_code != 200:
        print(f'Error obteniendo la prediccion {url}')
        print(f'Status Code = {prediccion.status_code}')
        return None
    
    soup_prediccion = BeautifulSoup(prediccion.text, 'lxml')
    
    horos_dict = scrap_horos(soup_prediccion)
    horos_dict['url'] = url

    return horos_dict

# Tercer Script.
def obtener_predicciones(soup):
    lista_predicciones = []
        
    # Obtenemos la lista de recetas.
    signos = soup.find('section', attrs={'class':'col-xs-12 col-md-8'}).find_all('a')
    for signo in signos:
        enlace = signo.get('href') 
        lista_predicciones.append(enlace)
    
    return lista_predicciones

# Cuarto Script.
predicciones = []
for i, link in enumerate(links_secciones):
    if i == 47:
        try:
            r = requests.get(link)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'lxml')
                predicciones.extend(obtener_predicciones(soup))
            else:
                print('No se pudo obtener la seccion', link)
        except Exception as e:
            print('No se pudo obtener la seccion', link)

# Script haciendo uso de Pandas.
data = []

enlace_final = 'https://www.hola.com/horoscopo/piscis/'

for i, prediccion in enumerate(predicciones):
    print(f'Scrapeando la nota {i}/{len(predicciones)}')
    data.append(scrape_prediccion('https://www.hola.com' + prediccion))

    # Detener el bucle si se alcanza el enlace final
    if 'https://www.hola.com' + prediccion == enlace_final:
        break


# Variable de Pandas.
dataframe = pd.DataFrame(data)
dataframe.to_excel('predicciones.xlsx', index=False, engine='xlsxwriter')
        




