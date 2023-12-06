import re
import math
import logging
import requests
import spacy
from bs4 import BeautifulSoup
from celery import shared_task
from .models import Article, Tag


@shared_task()
def crawel_news():
    logging.info('craweling news from diferent post source')

    def fetch_html(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch HTML from {url}: {e}")
            return None
    def calculate_reading_time(text):
        words = re.findall(r'\w+', text)
        word_count = len(words)

        # Average reading speed in words per minute
        words_per_minute = 300

        reading_time_minutes = word_count / words_per_minute
        reading_time_minutes = math.ceil(reading_time_minutes)
        return reading_time_minutes

    def extract_keywords(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        return keywords
    
    def fetch_articles_from_api(base_url, top, skip):
        api_url = f"https://www.who.int/api/hubs/newsitems?sf_site=15210d59-ad60-47ff-a542-7ed76645f0c7&sf_provider\
                    =OpenAccessDataProvider&sf_culture=en&$orderby=PublicationDateAndTime%20desc&$select=ItemDefaultUrl,\
                    ThumbnailUrl,FormatedDate&$format=json&$top={top}&$skip={skip}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('value', [])
        return []

    def extract_article_data(article_url, thumbnail_url):
        html_content = fetch_html(f"https://www.who.int/news/item{article_url}")
        soup = BeautifulSoup(html_content, 
                             'html.parser')
        title_header = soup.find('div', 
                                 {'class': 'sf-item-header-wrapper'})
        title = title_header.find('h1').text.strip() if title_header else ''

        body_div = soup.find('article', 
                             {'class': 'sf-detail-body-wrapper'})
        nested_paragraphs = []
        if body_div:
            divs = body_div.find_all('div')
            for div in divs:
                paragraphs = div.find_all('p')
                for paragraph in paragraphs:
                    nested_paragraphs.append(paragraph.text.strip())

        body = '\n'.join(nested_paragraphs)
        read_time = calculate_reading_time(body)
        keywords = extract_keywords(body)

        article_data = {
            'title': title,
            'thumbnail_url': thumbnail_url,
            'link': article_url,
            'read_time': read_time,
            'body': body,
            'keywords': keywords
        }

        return article_data

    def save_to_database(data):
        for article_data in data:

            # Create an Article object
            article = Article(
                headline=article_data['title'],
                body=article_data['body'],
                image_url=article_data['thumbnail_url'],
                read_time=article_data['read_time'],
                keywords=article_data['keywords'],
                link=f"https://www.who.int/news/item{article_data['link']}"
            )
            # Save the Article object to the database
            article.save()


    base_url = "https://www.who.int/news/item/"
    top = 100
    skip = 0
    total_articles = 1000  # Specify the total number of articles you want to fetch

    all_articles = []
    while skip < total_articles:
        articles = fetch_articles_from_api(base_url, top, skip)
        if not articles:
            break
        for article in articles:
            article_url = article.get('ItemDefaultUrl', '')
            thumbnail_url = article.get('ThumbnailUrl','')
            article_data = extract_article_data(article_url, thumbnail_url)
            all_articles.append(article_data)
            if len(all_articles) >= total_articles:
                break #stop if the total number of articles is reached
        skip += top

        save_to_database(all_articles)

        # while True:      # crawel the whole database
        #     articles = fetch_articles_from_api(base_url, top, skip)
        #     if not articles:
        #         break
        #     for article in articles:
        #         article_url = article.get('ItemDefaultUrl', '')
        #         print(article,'$$$$$$$$$$$$$$$$$$$$$$$')
        #         article_data = extract_article_data(article_url)
        #         all_articles.append(article_data)
        #     skip += top 
