from better_profanity import profanity
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import ValidationError, IntegerField, HiddenField, SubmitField, StringField
from wtforms.validators import Length, DataRequired, NumberRange

import cs235flix.movies.services as services
import cs235flix.utilities.utilities as utilities

import cs235flix.adapters.repository as repo
from cs235flix.authentication.authentication import login_required

movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 30

    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve all movies from the genre
    movies_all = services.get_all_movies_by_genre(genre_name, repo.repo_instance)

    # Retrieve the batch of movies to display on the Web page.
    movies_selected = services.get_selected_movies_by_genre(genre_name, cursor, movies_per_page, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movies_all):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movies_all) / movies_per_page)
        if len(movies_all) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews
    for movie in movies_selected:
        movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor,
                                           view_reviews_for=movie['rank'])
        movie['add_review_url'] = url_for('movies_bp.review_movie', rank=movie['rank'], cursor=cursor,
                                          genre=genre_name)
        movie['add_to_watchlist_url'] = url_for('movies_bp.add_to_watchlist', rank=movie['rank'])

    # Generate the webpage to display the movies by genre.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title=genre_name + " Movies",
        movies=movies_selected,
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
    )


@movies_blueprint.route('/review_movie', methods=['GET', 'POST'])
@login_required
def review_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with a movie rank, when subsequently called with a HTTP POST request, the movie rank remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the rank, representing the reviewed movie, from the form.
        rank = int(form.rank.data)
        genre = form.genre.data
        cursor = form.cursor.data

        # Use the service layer to store the new review.
        services.add_review(rank, username, form.review.data, form.rating.data, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same genre as the reviewed movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movies_bp.movies_by_genre', genre=genre, view_reviews_for=rank, cursor=cursor))

    if request.method == 'GET':

        # Request is a HTTP GET to display the form.
        # Extract the rank representing the movie to review from a query parameter of the GET request.
        rank = int(request.args.get('rank'))
        genre = request.args.get('genre')
        cursor = int(request.args.get('cursor'))

        # Store the rank in the form.
        form.rank.data = rank
        form.genre.data = genre
        form.cursor.data = cursor

    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the rank of the movie being reviewed from the form.
        rank = int(form.rank.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie_by_rank(rank, repo.repo_instance)
    return render_template(
        'movies/review_movie.html',
        title='Review Movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_movie'),
        genre_urls=utilities.get_genres_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = StringField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=10, message="Your rating must be between 1 and 10")])
    rank = HiddenField('Rank')
    genre = HiddenField('Genre')
    cursor = HiddenField('Cursor')
    submit = SubmitField('Submit')


@movies_blueprint.route('/search', methods=['GET', 'POST'])
def search_for_movie():
    # Create form.
    form = SearchForm()
    # Initialise empty list for final list of movies
    final_movies = list()

    if form.validate_on_submit():
        # Successful POST,
        # Extract the info ie. actor, genre and director from the form.
        actor = form.actor.data
        genre = form.genre.data
        director = form.director.data
        return redirect(url_for('movies_bp.search_results', actor=actor, genre=genre, director=director))

    return render_template(
        'movies/search_movie.html',
        title='Search for Movie',
        movie=final_movies,
        form=form,
        handler_url=url_for('movies_bp.search_for_movie'),
        genre_urls=utilities.get_genres_and_urls()
    )


class SearchForm(FlaskForm):
    actor = StringField('Actor')
    genre = StringField('Genre')
    director = StringField('Director')
    submit = SubmitField('Search')


@movies_blueprint.route('/search_results', methods=['GET', 'POST'])
def search_results():
    actor = request.args.get('actor')
    genre = request.args.get('genre')
    director = request.args.get('director')

    # empty form
    if actor == "" and genre == "" and director == "":
        return redirect(url_for('movies_bp.search_for_movie'))

    # retrieve all movies from service layer
    movies = services.get_movies(repo.repo_instance)
    # create list for movies that meet search criteria
    final_movies = list()

    # only actor
    if actor != "" and genre == "" and director == "":
        for movie in movies:
            if actor in movie['actors']:
                final_movies.append(movie)
    # actor and genre
    elif actor != "" and genre != "" and director == "":
        for movie in movies:
            if actor in movie['actors'] and genre in movie['genres']:
                final_movies.append(movie)
    # actor and director
    elif actor != "" and genre == "" and director != "":
        for movie in movies:
            if actor in movie['actors'] and movie['director'] == director:
                final_movies.append(movie)
    # genre and director
    elif actor == "" and genre != "" and director != "":
        for movie in movies:
            if genre in movie['genres'] == genre and movie['director'] == director:
                final_movies.append(movie)
    # genre
    elif actor == "" and genre != "" and director == "":
        for movie in movies:
            if genre in movie['genres']:
                final_movies.append(movie)
    # director
    elif actor == "" and genre == "" and director != "":
        for movie in movies:
            if movie['director'] == director:
                final_movies.append(movie)
    # all
    elif actor != "" and genre != "" and director != "":
        for movie in movies:
            if actor in movie['actors'] and genre in movie['genres'] and movie['director'] == director:
                final_movies.append(movie)

    # Read query parameters.
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')
    movies_per_page = 30

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    # Retrieve the batch of movies to display on the Web page.
    movies_selected = services.get_selected_movies(cursor, movies_per_page, final_movies, repo.repo_instance)

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.search_results', actor=actor, genre=genre, director=director,
                                 cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.search_results', actor=actor, genre=genre, director=director)

    if cursor + movies_per_page < len(final_movies):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.search_results', actor=actor, genre=genre, director=director,
                                 cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(final_movies) / movies_per_page)
        if len(final_movies) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.search_results', actor=actor, genre=genre, director=director,
                                 cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews
    for movie in movies_selected:
        movie['view_review_url2'] = url_for('movies_bp.search_results', actor=actor, genre=genre, director=director,
                                            cursor=cursor, view_reviews_for=movie['rank'])
        movie['add_review_url2'] = url_for('movies_bp.review_movie_search', rank=movie['rank'], cursor=cursor,
                                           actor=actor, genre=genre, director=director)
        movie['add_to_watchlist_url2'] = url_for('movies_bp.add_to_watchlist', rank=movie['rank'])

    return render_template(
        'movies/search_results.html',
        title='Search Results',
        movies=movies_selected,
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movies_blueprint.route('/review_movie_search', methods=['GET', 'POST'])
@login_required
def review_movie_search():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with a movie rank, when subsequently called with a HTTP POST request, the movie rank remains in the
    # form.
    form = ReviewForm2()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the rank, representing the reviewed movie, from the form.
        rank = int(form.rank.data)
        genre = form.genre.data
        cursor = form.cursor.data
        actor = form.actor.data
        director = form.director.data
        print(actor, genre, director)

        # Use the service layer to store the new review.
        services.add_review(rank, username, form.review.data, form.rating.data, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same genre as the reviewed movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movies_bp.search_results', genre=genre, actor=actor, director=director,
                                view_reviews_for=rank, cursor=cursor))

    if request.method == 'GET':

        # Request is a HTTP GET to display the form.
        # Extract the rank representing the movie to review from a query parameter of the GET request.
        rank = int(request.args.get('rank'))
        genre = request.args.get('genre')
        cursor = int(request.args.get('cursor'))
        actor = request.args.get('actor')
        director = request.args.get('director')

        # Store the info in the form
        form.rank.data = rank
        form.genre.data = genre
        form.cursor.data = cursor
        form.actor.data = actor
        form.director.data = director

    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the rank of the movie being reviewed from the form.
        rank = int(form.rank.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie_by_rank(rank, repo.repo_instance)
    return render_template(
        'movies/review_movie.html',
        title='Review Movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_movie_search'),
        genre_urls=utilities.get_genres_and_urls()
    )


class ProfanityFree2:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm2(FlaskForm):
    review = StringField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=10, message="Your rating must be between 1 and 10")])
    rank = HiddenField('Rank')
    genre = HiddenField('Genre')
    cursor = HiddenField('Cursor')
    actor = HiddenField('Actor')
    director = HiddenField('Director')
    submit = SubmitField('Submit')


@movies_blueprint.route('/add_to_watchlist', methods=['GET', 'POST'])
@login_required
def add_to_watchlist():
    username = session['username']
    rank = int(request.args.get('rank'))

    services.add_movie_to_watchlist(username, rank, repo.repo_instance)
    return redirect(url_for('movies_bp.watchlist', user=username))


@movies_blueprint.route('/watchlist', methods=['GET', 'POST'])
@login_required
def watchlist():
    username = session['username']
    user_watchlist = services.get_watchlist_for_user(username, repo.repo_instance)

    for movie in user_watchlist:
        movie['remove_from_watchlist'] = url_for('movies_bp.remove_from_watchlist', rank=movie['rank'])

    return render_template(
        'movies/watchlist.html',
        title='Watchlist',
        user_watchlist=user_watchlist,
        genre_urls=utilities.get_genres_and_urls(),
    )


@movies_blueprint.route('/remove_from_watchlist', methods=['GET', 'POST'])
@login_required
def remove_from_watchlist():
    username = session['username']
    rank = int(request.args.get('rank'))
    services.remove_movie_from_watchlist(username, rank, repo.repo_instance)

    return redirect(url_for('movies_bp.watchlist', user=username))
