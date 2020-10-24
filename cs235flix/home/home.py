from flask import Blueprint, render_template

from cs235flix.utilities import utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        genre_urls=utilities.get_genres_and_urls()
    )
