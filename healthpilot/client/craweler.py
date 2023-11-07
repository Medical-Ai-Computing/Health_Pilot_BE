import requests
import os
import csv
import json
from bs4 import BeautifulSoup

def fetch_html(url):
    """
    Fetches the HTML content of the given URL.
    """
    response = requests.get(url)
    # print(response.text)
    return response.text

def extract_articles(html_content):
    """
    Extracts news articles' titles and bodies from the given HTML content using BeautifulSoup.
    """
    # Parse the JSON-like content

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title from <h1> element
    title_header = soup.find('div', {'class': 'sf-item-header-wrapper'})
    title = title_header.find('h1').text.strip() if title_header else ''

    # Extract body from <div class="sf_colsIn col-md-8"> and <p> elements
    body_div = soup.find('article', {'class': 'sf-detail-body-wrapper'})
    nested_paragraphs = []
    if body_div:
        divs = body_div.find_all('div')
        for div in divs:
            paragraphs = div.find_all('p')
            for paragraph in paragraphs:
                nested_paragraphs.append(paragraph.text.strip())
    
    article_data = {
        'title': title,
        'body': '\n'.join(nested_paragraphs)
    }

    print(f'\n\nTitle: {article_data["title"]}\nBody: {article_data["body"]}')
    return article_data


def crawl_website(url):
    """
    Crawls the given website and extracts news articles' titles and bodies.
    """
    html_content = fetch_html(url)
    articles = extract_articles(html_content)

    return articles

if __name__ == "__main__":
    target_url = 'https://www.who.int/news/item/07-11-2023-who-launches-guide-on-whole-genome-sequencing-use-as-a-tool-for-foodborne-disease-surveillance-and-response'
    news_articles = crawl_website(target_url)

