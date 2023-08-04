import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

# Variables de trabajo.

# URL a usar.
url =  'https://www.directoalpaladar.com/'

# Encapsulamos el request a la url en una variable.
direct_palad = requests.get(url)

# Volvemos una soup nuestra variable encapsulada.
s_palad = BeautifulSoup(direct_palad.text, 'lxml')

# Ubicamos las secciones dentro de la pagina we.
secciones = s_palad.find('nav', attrs={'class':'head-primary'}).find_all('li')

# Dividimos las secciones en secciones individuales y seleccionamos la que queremos trabajar.
seccion = secciones[3]

'''
secciones:
0 - Postres
1 - Viajes
2 - Seleccíon
3 - Vegui
'''

# Ahora, tomamos los links de las secciones.
links_secciones = [seccion.a.get('href') for seccion in secciones]

# Luego, elegimos el link de la seccion que vamos a usar.
link_trabajo = requests.get(links_secciones[3])

# Convertimos el link en una soup.
s_linktrabajo = BeautifulSoup(link_trabajo.text, 'lxml')

# Obtenemos la lista de recetas.
lista_recetas = s_linktrabajo.find_all('h2', attrs={'class':'abstract-title'})

# Tomamos los links de las recetas.
enlaces_recetas = [receta.a.get('href') for receta in lista_recetas]

# Aqui podemos tomar links individuales.
enlace_receta = enlaces_recetas[5]

# Scripts de Trabajo.
try:
    def scrap_palad(s_receta):
        receta_dict = {}

        Fecha = s_receta.find('time', attrs={'class': 'article-date'})
        if Fecha:
            Fecha_str = Fecha.text.strip()
            # Convertir la fecha en formato ISO 8601 a un formato más simple de leer
            Fecha_datetime = datetime.fromisoformat(Fecha_str.replace('Z', '+00:00'))
            receta_dict['Fecha'] = Fecha_datetime.strftime('%d/%m/%Y %H:%M')
        else:
            receta_dict['Fecha'] = None

        Titulo = s_receta.find('h1')
        if Titulo:
            receta_dict['Titulo'] = Titulo.text.strip()
        else:
            receta_dict['Titulo'] = None

        Autor = s_receta.find('a', attrs={'class': 'article-author-link'})
        if Autor:
            receta_dict['Autor'] = Autor.text.strip()
        else:
            receta_dict['Autor'] = None
        
        Ingredientes = s_receta.find('ul', attrs={'class': 'asset-recipe-list'})
        if Ingredientes:
            receta_dict['Ingredientes'] = Ingredientes.text.strip().replace('\n', '')
        else:
            receta_dict['Ingredientes'] = None
        
        Preparacion = s_receta.find('div', attrs={'class': 'asset-recipe-steps'})
        if Preparacion:
            receta_dict['Preparacion'] = Preparacion.text.strip().replace('\n', '')
        else:
            receta_dict['Preparacion'] = None

        return receta_dict



except Exception as e:
    print('Error:')
    print(e)
    print('\n')

# Segundo Script.
def scrape_receta(url):
    try:
        receta = requests.get(url)
    except Exception as e:
        print('Error scrapeando URL', url)
        print(e)
        return None
    
    if receta.status_code != 200:
        print(f'Error obteniendo nota {url}')
        print(f'Status Code = {receta.status_code}')
        return None
    
    soup_receta = BeautifulSoup(receta.text, 'lxml')
    
    receta_dict = scrap_palad(soup_receta)
    receta_dict['url'] = url

    return receta_dict

# Tercer Script.
def obtener_recetas(soup):
    lista_recetas = []
        
    # Obtenemos la lista de recetas.
    recetas = soup.find_all('h2', attrs={'class':'abstract-title'})
    for receta in recetas:
        enlace = receta.a.get('href') # Buscamos el enlace dentro del elemento h2
        lista_recetas.append(enlace)
    
    return lista_recetas


# Cuarto Script.
recetas = []
for i, link in enumerate(links_secciones):
    # Verificar si la sección actual es "Vegui"
    if i == 3:
        try:
            r = requests.get(link)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'lxml')
                recetas.extend(obtener_recetas(soup))
            else:
                print('No se pudo obtener la seccion', link)
        except Exception as e:
            print('No se pudo obtener la seccion', link)


# Script haciendo uso de Pandas.
data = []
for i, receta in enumerate(recetas):
    print(f'Scrapeando la nota {i}/{len(recetas)}')
    data.append(scrape_receta(receta))

# Variable de Pandas.
dataframe = pd.DataFrame(data)
dataframe.to_excel('recetas.xlsx', index=False, engine='xlsxwriter')
dataframe['Fecha'] = pd.to_datetime(dataframe['Fecha'], format='%d/%m/%Y %H:%M')


recetas_data = dataframe.to_dict(orient='records')

# Logica de vinculacion con la API.

# URL de la API para enviar los datos
api_url = 'http://127.0.0.1:8000/api/Recetas/'  # Reemplaza esto con la URL de tu API

# Realizar la solicitud GET a la API para obtener la lista de títulos ya enviados
response = requests.get(api_url)
existing_recetas = []

if response.status_code == 200:
    existing_recetas = [receta['Titulo'] for receta in response.json()]

# Realizar la solicitud POST a la API
headers = {'Content-Type': 'application/json'}

for _, receta in dataframe.iterrows():
    receta_data = {
        "Fecha": receta["Fecha"].strftime('%Y-%m-%dT%H:%M:%S'),  # Formatear la fecha en el formato deseado
        "Titulo": receta["Titulo"][:100],  # Limitar el título a 100 caracteres
        "Autor": receta["Autor"],
        "Ingredientes": receta["Ingredientes"],
        "Preparacion": receta["Preparacion"],
        "url": receta["url"]
    }

    # Verificar si el título de la receta ya existe en la lista de enviados
    if receta_data["Titulo"] in existing_recetas:
        print(f'Receta "{receta_data["Titulo"]}" ya existe en la API. No se enviará nuevamente.')
    else:
        # Verificar que los campos "Ingredientes" y "Preparacion" no estén vacíos
        if pd.notna(receta_data["Ingredientes"]) and pd.notna(receta_data["Preparacion"]):
            response = requests.post(api_url, json=receta_data, headers=headers)

            # Verificar si la solicitud fue exitosa para cada receta individual
            if response.status_code == 201:
                print(f'Receta "{receta_data["Titulo"]}" enviada exitosamente a la API.')
                existing_recetas.append(receta_data["Titulo"])  # Agregar el título a la lista de enviados
            else:
                print(f'Error al enviar la receta "{receta_data["Titulo"]}" a la API. Para mas informacion puedes consultar en "{receta_data["url"]}')
                print(response.text)
        else:
            print(f'Error: Los campos "Ingredientes" y "Preparacion" no pueden estar vacíos para la receta "{receta_data["Titulo"]}". Para mas informacion puedes consultar en "{receta_data["url"]}')