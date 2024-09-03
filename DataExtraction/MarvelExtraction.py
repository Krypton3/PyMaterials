import csv
import json
import requests
from bs4 import BeautifulSoup


def extract():
    id = ['0371746', '0800080', '1228705', '0800369', '0458339']

    # Headers: A dictionary of headers like content-type, date, server, etc.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    with open('marvel.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['movie_name', 'movie_year', 'movie_rating_type', 'movie_description', 'movie_keywords',
                         'movie_genre', 'movie_actors', 'movie_rating_user', 'movie_rating', 'direction', 'writers',
                         'storyline'])

        for movie_ids in id:
            # base url
            page_link = "https://www.imdb.com/title/tt" + movie_ids + "/"
            # request to get html/json content of the base url with a code
            page_response = requests.get(page_link, headers=headers, timeout=5)
            if page_response.status_code == 403:
                print(f"Access denied to {page_link}.")
                continue

            # BeautifulSoup to extract data from HTML
            page_content = BeautifulSoup(page_response.content, "html.parser")
            script_tag = page_content.find('script', type='application/ld+json')

            if script_tag is None:
                print(f"No ld+json script tag found for {page_link}")
                continue
            data = json.loads(script_tag.string)

            # fetching basic movie informations
            movie_name = data['name']
            movie_year = data['datePublished']
            movie_rating_type = data.get('contentRating', 'N/A')
            movie_description = data['description']
            movie_keywords = data.get('keywords', 'N/A')
            movie_genre = data.get('genre', 'N/A')
            movie_rating_user = data['aggregateRating']['ratingCount']
            movie_rating = data['aggregateRating']['ratingValue']

            # fetching stars, direction, and writers
            stars = [actor['name'] for actor in data['actor']]
            direction = [director['name'] for director in data['director']] if isinstance(data['director'], list) else [data['director']['name']]
            writers = [creator['name'] for creator in data['creator'] if 'name' in creator]

            # fetching storyline with specific div and class
            get = page_content.find('div', attrs={"class": "ipc-html-content ipc-html-content--base"})
            storyline = get.text if get else 'N/A'

            writer.writerow([movie_name, movie_year, movie_rating_type, movie_description, movie_keywords, movie_genre,
                            stars, movie_rating_user, movie_rating, direction, writers, storyline])
