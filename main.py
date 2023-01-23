import sqlite3


def search(title):
    """
        Функция, которая выполняет поиск фильма и возвращает в формате:
                {
                "title": "title",
                "country": "country",
                "release_year": 2021,
                "genre": "listed_in",
                "description": "description"
        }.
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title  LIKE '%{title}%'  
        """
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            title_json = {
                    "title": row[0],
                    "country": row[1],
                    "release_year": row[2],
                    "listed_in": row[3],
                    "description": row[4]
                }
            return title_json


def search_by_year(from_year, to_year):
    """
        Функция, которая выполняет поиск фильмов в диапазоне лет выпуска
        ивозвращает в формате:
                      [
            {"title":"title",
             "release_year": 2021},
            {"title":"title",
             "release_year": 2020}
        ]
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN '{from_year}' AND '{to_year}'
            AND type = 'Movie'
            LIMIT 100
        """
        cursor.execute(query)
        results = []
        for data in cursor.fetchall():
            result = {
                "title": data[0],
                "release_year": data[1],
            }
            results.append(result)
        return results


def get_rating(group):
    """
    Функция поиска по рейтингу.
    :param group: children, family, adult.
    :return: рейтинг.
    """
    if group.lower() == 'children':
        return 'G', 'G'
    elif group.lower() == 'family':
        return 'G', 'PG', 'PG-13'
    elif group.lower() == 'adult':
        return 'R', 'NC-17'
    else:
        return 'Dont know this group'


def get_rating_query(rating):
    """
    Функция, которая принимает список допустимых рейтингов и
    возвращала данные в формате списка словарей.
    :param rating: данные рейтинга (get_rating(group)).
    :return: данные в формате списка словарей.
    """
    # SQL запрос.
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        try:
            query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating IN {rating} AND type = 'Movie' 
            """
            results = []
            cursor.execute(query)
            for data in cursor.fetchall():
                result = {
                    "title": data[0].strip("\n"),
                    "rating": data[1].strip("\n"),
                    "description": data[2].strip("\n"),
                }
                results.append(result)
        except IndexError:
            return []
        return results


def get_genre(genre):
    """
    Функция, которая получает название жанра
    и возвращает 10 самых свежих фильмов в формате json.
    :param genre: Жанр фильма.
    :return: Возвращает 10 самых свежих фильмов в формате json.
    """
    with sqlite3.connect('./netflix.db') as connection:
        cursor = connection.cursor()
        # Фильтрация по результатам агрегации и группировки.
        try:
            query = f"""
                SELECT title, description
                FROM netflix
                WHERE listed_in LIKE '%{genre}%'
                AND type LIKE '%Movie%' 
                ORDER BY release_year DESC
                LIMIT 10
            """
            results = []
            for data in cursor.execute(query).fetchall():
                result = {
                    "title": data[0].strip("\n"),
                    "description": data[1].strip("\n"),
                }
                results.append(result)
        except IndexError:
            results = []
        return results

#print(get_genre("horror"))
#print(search("Jacob"))
#print(search_by_year(2000,2001))