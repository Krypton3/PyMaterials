import os
import time
from celery import Celery

from bs4 import BeautifulSoup
import requests
import json
import csv

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name='tasks.extraction')
def extraction():
    start_time = time.time()
    id = ['0371746', '0800080', '1228705', '0800369', '0458339']

    # id = ['5095030']
    with open('marvel.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['movie_name', 'movie_year', 'movie_rating_type', 'movie_description', 'movie_keywords',
                        'movie_genre', 'movie_actors', 'movie_rating_user', 'movie_rating', 'direction', 'writers',
                        'storyline'])

        track = 0
        while track < len(id):
            page_link = "http://www.imdb.com/title/tt"+str(id[track])
            page_response = requests.get(page_link, timeout=5)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            data = json.loads(page_content.find('script', type='application/ld+json').text)

            get = page_content.find('span', attrs={"class": "TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex"})
            movie_year = get.text

            movie_name = data['name']
            movie_rating_type = data['contentRating']
            movie_description = data['description']
            movie_keywords = data['keywords']
            movie_genre = data['genre']
            movie_actors = len(data['actor'])
            movie_rating_user = data['aggregateRating']['ratingCount']
            movie_rating = data['aggregateRating']['ratingValue']

            i = 0
            stars = []
            while i < movie_actors:
                stars.append(data['actor'][i]['name'])
                i = i + 1

            direction = []
            if type(data['director']) == list:
                dict = len(data['director'])
                i = 0
                while i < dict:
                    if 'name' in data['director'][i]:
                        direction.append(data['director'][i]['name'])
                    i = i + 1
            else:
                direction.append(data['director']['name'])

            writers = []
            if type(data['creator']) == list:
                dict = len(data['creator'])
                i = 0
                while i < dict:
                    if 'name' in data['creator'][i]:
                        writers.append(data['creator'][i]['name'])
                    i = i + 1
            else:
                writers.append(data['creator']['name'])

            get = page_content.find('div', attrs={"class": "ipc-html-content ipc-html-content--base"})
            storyline = get.text

            writer.writerow([movie_name, movie_year, movie_rating_type, movie_description, movie_keywords, movie_genre,
                            stars, movie_rating_user, movie_rating, direction, writers, storyline])

            track = track + 1
    return "The time required to extract information: " + str(time.time() - start_time) + " seconds"