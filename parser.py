from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

import requests
from bs4 import BeautifulSoup

OLX_DOMAIN = 'https://www.olx.ua'


def parse_list(url):
    soup = get_soup_from_url(url)

    ads = soup.find_all(attrs={"data-cy": "l-card"})

    result = []
    for ad in ads:
        result.append({
            'url': OLX_DOMAIN + ad.find('a').get('href'),
            'name': ad.find('h6').text,
            'price': ad.find('p').text,
            'img': ad.find('img').get('src', ''),
        })

    with ThreadPoolExecutor() as executor:
        result = executor.map(parse_ad, result)

    return list(filter(None, result))


def parse_ad(ad):
    if 'no_thumbnail' in ad['img']:
        soup = get_soup_from_url(ad['url'])
        img = soup.find('img')
        if not img:
            return None
        ad['img'] = img.get('src', '')

    del ad['url']

    return ad


def get_soup_from_url(url):
    print('goto:', url)
    r = requests.get(url)
    html = r.content
    return BeautifulSoup(html, 'html.parser')


def parse_all_data():
    urls = [
        f'{OLX_DOMAIN}/d/nedvizhimost/kvartiry' 
        f'/dolgosrochnaya-arenda-kvartir/khmelnitskiy/' 
        f'?currency=UAH&search%5Border%5D=created_at%3Adesc&page={i + 1}' for i in range(3)
    ]

    with ThreadPoolExecutor() as executor:
        results = executor.map(parse_list, urls)

    # pprint(results)

    total_res = []
    for result in results:
        total_res = total_res + result

    total_res = total_res[:100]

    return total_res

#
# if __name__ == '__main__':
#     pprint(parse_all_data())
#
#     # pprint(parse_ad({
#     #     'img': 'no_thumbnail',
#     #     'url': 'https://www.olx.ua/d/uk/obyavlenie/prodazh-1k-kvartiri-v-zdanomu-dom-zhk-berezhanskiy-vul-gulaka-4-IDPaTK5.html',
#     # }))
