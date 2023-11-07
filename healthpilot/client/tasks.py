from celery import shared_task
from .models import Article, Tag
import logging


@shared_task()
def crawel_news():
    logging.info('craweling news from diferent post source')
    print("test tasks for celery print function")

