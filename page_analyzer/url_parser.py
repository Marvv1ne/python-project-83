import requests
from bs4 import BeautifulSoup

def get_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1').text[:255] if soup.find('h1') else ''
    title = soup.find('title').text[:255] if soup.find('title') else ''
    description = soup.find('meta', attrs={'name': 'description'}).get('content', '') if soup.find('meta', attrs={'name': 'description'}) else '';
    return {
        'status_code': response.status_code,
        'h1': h1,
        'title': title,
        'description': description
    }
