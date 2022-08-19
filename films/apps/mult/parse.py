import requests, json
from bs4 import BeautifulSoup
from django.conf import settings


def kinopoiskParse(film_id):
    url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/" + film_id
    response = json.loads(requests.get(url, headers={'Accept': 'application/json',
                                                     'X-API-KEY': settings.SECRETS[0]}).text)
    seasons = 0
    id_last_season = 0
    film = response['data']
    film['genres'] = [genre['genre'].capitalize() for genre in film['genres']]
    if film['seasons']:
        for i, season in enumerate(film['seasons']):
            if season['number'] >= seasons:
                seasons = int(season['number'])
                id_last_season = i
        for serie in film['seasons'][id_last_season]['episodes']:
            if serie['releaseDate'] is None and serie['episodeNumber'] == 1:
                seasons -= 1
    else:
        seasons = "Фильм"
    if film['type'] == 'TV_SHOW':
        film_type = "Сериал"
    elif film['type'] == 'FILM':
        film_type = "Фильм"
    else:
        film_type = film['type']
    countries = ''
    episodes = 1
    for country in film['countries']:
        countries += country['country'] + " "
    status = "Вышло " + str(film['year'])
    if not film["nameRu"] and film["nameEn"]:
        name = film["nameEn"]
    else:
        name = film["nameRu"]
    return {'name': name,
             'country': countries.strip(),
             'seasons': seasons,
             'type': film_type,
             'year': film['year'],
             'img': film['posterUrl'],
             'genre': film['genres'],
             'status': status,
             'episodes': episodes,
             'description': film['description'],
             'isShown': True}


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
           'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, timeout=(3, 10))
    if r.status_code != 200:
        return ConnectionAbortedError
    return r


def shikimoriParse(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    name = soup.find('h1').get_text()
    status = ''
    eps = "Фильм"
    item = soup.find('div', class_='b-db_entry')
    img = item.find('img').get('src')
    img = img[0:img.find("?")]
    info = soup.find_all('div', class_='line-container')
    for item in info:
        if item.find('div', class_='key') is not None:
            a = item.find('div', class_='key').get_text()
            if a == 'Эпизоды:':
                eps = item.find('div', class_='value').get_text()
            elif a == 'Статус:':
                status = item.find('span', class_='b-anime_status_tag').get('data-text') + item.find('div', class_='value').get_text()
            elif a == 'Жанры:':
                genre = []
                for n in item.find_all('span', class_='genre-ru'):
                    genre.append(n.get_text().capitalize())
                break
    if soup.find('div', class_='b-text_with_paragraphs'):
        desc = soup.find('div', class_='b-text_with_paragraphs').get_text()
    else:
        desc = "Нет описания"
    return {
        'name': name,
        'episodes': eps,
        'status': status,
        'description': desc,
        'genre': genre,
        'img': img,
        'isShown': True
    }
