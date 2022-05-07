import requests
from bs4 import BeautifulSoup


def get_weather(pos):
    url = f'https://www.google.com/search?q=+weather{pos}'
    html = requests.get(url).content
    try:
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find(
            'div',
            attrs={'class': 'BNeawe iBp4i AP7Wnd'}
        ).text
        info = soup.find(
            'div',
            attrs={'class': 'BNeawe tAd8D AP7Wnd'}
        ).text
    except:
        return ['Not found']
    data = info.split('\n')
    return [temp, data[0], data[1]]
