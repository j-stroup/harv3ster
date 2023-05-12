import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

urls_to_visit = []
visited_urls = []


# Parse HTML
def get_linked_urls(url, html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find linked urls
    links = soup.find_all('a')
    for link in links:
        path = link.get('href')
        if path and path.startswith('/'):
            path = urljoin(url, path)
        if path and path.endswith('.jpg'):
            pass
        else:
            yield path

    # Find <p> text
    ptags = soup.find_all('p')
    for soup in ptags:
        text = re.sub("[\<].*?[\>]", "", str(soup)).strip()
        if text != '' and text.endswith('.') or text.endswith('?') or text.endswith('!'):
            with open('words.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{text}')
                f.close()

# Add discovered url to list if not already crawled
def add_url_to_visit(url):
    if url not in visited_urls and url not in urls_to_visit:
        urls_to_visit.append(url)

# Request url and grab html
def crawl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    html = requests.get(url, headers=headers).text
    time.sleep(.5)
    for url in get_linked_urls(url, html):
        add_url_to_visit(url)

# Main function
def run():
    while urls_to_visit:
        url = urls_to_visit.pop(0)
        logging.info(f'Crawling: {url}')
        try:
            if url.startswith('http'):
                crawl(url)
            else:
                pass
        except Exception:
            logging.exception(f'Failed to crawl: {url}')
        finally:
            visited_urls.append(url)

# Select target(s)
def start():
    target_domain = input('Domain(s): https://')
    if target_domain != '':
        urls_to_visit.append('https://' + target_domain)
        start()
    run()

if __name__ == '__main__':
    start()
