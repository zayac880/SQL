from flask import Flask, jsonify
from main import search, search_by_year, get_rating, get_rating_query, get_genre

app = Flask(__name__)


@app.route('/<title>')
def search_title(title):
    """Возвращает фильм"""
    post = search(title)
    return post

@app.route('/year/<int:from_year>/to/<int:to_year>')
def get_year(from_year, to_year):
    """Возвращает фильм в диапазоне лет выпуска"""
    posts = search_by_year(from_year, to_year)
    return posts

@app.route('/rating/<group>/')
def get_group_page(group):
    """
    :param group: Возвращает возрастную группу: children, family, adult.
    :return: Возвращает содержащий информацию о названии, рейтинге и описании.
    """
    rating = get_rating(group)
    result = get_rating_query(rating)
    return jsonify(result)


@app.route('/genre/<genre>')
def genre(genre):
    """Возвращает фильмы по жанру"""
    post = get_genre(genre)
    return post


if __name__ == "__main__":
    app.run(debug=True, port=5010)