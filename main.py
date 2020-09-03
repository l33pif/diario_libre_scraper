import requests
from bs4 import BeautifulSoup
import pandas as pd


def main(url):
    links = _obtener_links(url)
    data = _obtener_data(links)
    _save_data(data)

def _obtener_links(url):
    diario = requests.get(url)
    links_ = []
    links = []
    
    if diario.status_code == 200:
        soup_diario = BeautifulSoup(diario.text, 'lxml')
        article_list = soup_diario.find_all('div', attrs={'class':'multimediaIconMacroWrapper C'})
        for article in article_list:
            if article:
                links_.append(article.a.get('href'))

    url_base = 'https://www.diariolibre.com/'
    for link in links_:
        link = url_base + link
        links.append(link)
    return links


def _obtener_data(links):
    data = []

    for i, nota in enumerate(links):
        print(f'Scrapeando nota {i}/{len(links)}')
        data.append(__scrape_nota(nota))
    return data


def __scrape_nota(url):
    try:
        nota = requests.get(url)
    except Exception as e:
        print(f'Error scrapeando ULR {url}')
        print(e)
        return None

    if nota.status_code != 200:
        print('fError obteniendo nota {url}')
        print(f'Status code = {nota.status_code}')
        return None

    soup_note = BeautifulSoup(nota.text, 'lxml')

    ret_dict = __obtener_info(soup_note)
    ret_dict['url'] = url

    return ret_dict


def __obtener_info(soup_note):
    info_dict = {}

    title = soup_note.find('span', attrs={'class':'priority-content'})
    if title:
        info_dict['title'] = title.text
    else:
        info_dict['title'] = None
    
    img_info = soup_note.find('div', attrs={'class':'img-info'})
    if img_info:
        info_dict['infoIMG'] = img_info.text
    else:
        info_dict['ingoIMG'] = None

    body = soup_note.find('div', attrs={'class':'paragraph'})
    if body:
        info_dict['body'] = body.text
    else:
        info_dict['body'] = None

    return info_dict


def _save_data(data):
    df = pd.DataFrame(data)
    df.to_csv('diario_libre.csv', encoding='utf-8')
        
    return df


if __name__ == "__main__":
    url = 'https://www.diariolibre.com/noticias-de-hoy'
    main(url)