from bs4 import BeautifulSoup
import requests
import json


PAGE = "https://mixx.io/page/"
URL_2022 = "/?orderby=post_date&order=desc&s=2022#038;order=desc&s=2022"
URL_2023 = "/?orderby=post_date&order=desc&s=2023#038;order=desc&s=2023"

resultado_json = []
index=0
page=1
error = False
while error==False:

    url = PAGE+str(page)+URL_2022
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Buscar un patrón específico o texto que indique un error 404 en el HTML
    if 'error404' in html_content or 'página no encontrada' in html_content.lower():
        print('Error 404: La página no fue encontrada.')
        error=True
    else:
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')


        rows = soup.find_all('div', class_='row mb-4')
        for row in rows:
            if '#Diario' in row.text:
                # Encuentra el elemento con clase 'col-4 col-md-3' para obtener la URL
                col = row.find('div', class_='col-4 col-md-3')
                url = col.find('a')['href'] if col and col.find('a') else 'URL no encontrada'
                h5_text = row.find('h5').get_text(strip=True) if row.find('h5') else 'Texto no encontrado'

                print(h5_text)
                
                resultado_json.append({'index': index, 'url': url, 'texto': h5_text})
                index += 1  # Incrementar el índice para la próxima entrada
        page += 1
        
        
with open('mixxio.2022'+'.json', 'w') as f:
    json.dump(resultado_json, f, ensure_ascii=False, indent=4)
#print(json_result)