import validators
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def validate_url(url):
    if len(url) > 255:
        return 'URL превышает 255 символов'
    elif not validators.url(url):
        return 'Некорректный URL'
    elif not url:
        return 'URL обязателен для заполнения'


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1').text[:255] if soup.find('h1') else ''
    title = soup.find('title').text[:255] if soup.find('title') else ''
    meta = soup.find('meta', attrs={'name': 'description'})
    description = (meta.get('content', '') if meta else '')
    return {
        'status_code': response.status_code,
        'h1': h1,
        'title': title,
        'description': description
    }
