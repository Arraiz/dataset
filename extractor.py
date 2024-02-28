from bs4 import BeautifulSoup
import requests
import json
import emoji


with open('mixxio.2023.json', 'r') as archivo_json:
    datos = json.load(archivo_json)

    for el in datos:
        print(el['url'])

        URL = el['url']
        html_content = requests.get(URL).text
        soup = BeautifulSoup(html_content, 'html.parser')

        articulos = soup.find_all('section', class_='mt-2 articulo')

        articulos_json = []
        index = 0

        def extraer_emojis_y_posiciones(texto):
            emojis_posiciones = [(char, pos) for pos, char in enumerate(texto) if emoji.is_emoji(char)]
            texto_sin_emojis = ''.join(char for char in texto if not emoji.is_emoji(char))
            return texto_sin_emojis, emojis_posiciones

                
        def format_URL(string):
            return string.replace("https://", "").replace('/', '-')


        for articulo in articulos:
            textos = []
            urls = []
            emojis_y_posiciones = []
            titulo = ''

            for elemento in articulo.contents:
                if elemento.name == 'p':
                    parrafo_texto = elemento.get_text(" ", strip=True).replace('COMPARTIR', '')
                    if elemento.find('strong'):
                        titulo = elemento.find('strong').get_text(strip=True)
                        parrafo_texto = parrafo_texto.replace(titulo, '').strip()
                    parrafo_sin_emojis, posiciones = extraer_emojis_y_posiciones(parrafo_texto)
                    textos.append(parrafo_sin_emojis)
                    emojis_y_posiciones.extend(posiciones)
                    
                    for a_tag in elemento.find_all('a', href=True):
                        if a_tag.text.strip().upper() != 'COMPARTIR':
                            urls.append(a_tag['href'])
                
                elif elemento.name == 'hr' and textos:
                    articulos_json.append({
                        'index': index,
                        'titulo': titulo,
                        'texto': textos,
                        'urls': urls,
                        'emojis': [{'emoji': e[0], 'posicion': e[1] + sum(len(t) + 1 for t in textos[:i])} for i, e in enumerate(emojis_y_posiciones)]
                    })
                    index += 1
                    textos = []
                    urls = []
                    emojis_y_posiciones = []

            if textos:
                articulos_json.append({
                    'index': index,
                    'titulo': titulo,
                    'texto': textos,
                    'urls': urls,
                    'emojis': [{'emoji': e[0], 'posicion': e[1] + sum(len(t) + 1 for t in textos[:i])} for i, e in enumerate(emojis_y_posiciones)]
                })


        name = format_URL(URL)
        with open("text-data/"+name+'.json', 'w') as f:
            json.dump(articulos_json, f, ensure_ascii=False, indent=4)