from typing import Iterable
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domainmodel.model import Movie, User, make_review, Review


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(rank: int, username: str, review_text: str, rating: int, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie_by_rank(rank)
    print(movie)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    review = make_review(user, movie, review_text, rating)

    # Update the repository.
    repo.add_review(review)


def add_movie_to_watchlist(username, rank, repo: AbstractRepository):
    movie = repo.get_movie_by_rank(rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Update the repository
    if movie not in user.watchlist:
        user.add_movie_to_watchlist(movie)


def remove_movie_from_watchlist(username, rank, repo: AbstractRepository):
    movie = repo.get_movie_by_rank(rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Update the repository
    user.remove_movie_from_watch_list(movie)


def get_watchlist_for_user(username, repo:AbstractRepository):
    user = repo.get_user(username)
    watchlist = user.watchlist
    return movies_to_dict(watchlist)


def get_user(username, repo: AbstractRepository):
    return repo.get_user(username)


def get_movies(repo: AbstractRepository):
    movies = repo.get_movies()
    return movies_to_dict(movies)


def get_reviews_for_movie(rank, repo: AbstractRepository):
    movie = repo.get_movie_by_rank(rank)
    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


def get_movie_by_rank(rank: int, repo: AbstractRepository):
    movie = repo.get_movie_by_rank(rank)
    if movie is None:
        raise NonExistentMovieException
    return movie_to_dict(movie)


def get_movie(title: str, repo: AbstractRepository):
    movie = repo.get_movie(title)
    if movie is None:
        raise NonExistentMovieException
    return movie_to_dict(movie)


def get_selected_movies_by_genre(genre, cursor, movies_per_page, repo: AbstractRepository):
    movies = repo.get_movies_by_genre(genre)
    movies_selected = movies[cursor:cursor + movies_per_page]
    movies_as_dict = movies_to_dict(movies_selected)
    return movies_as_dict


def get_selected_movies(cursor, movies_per_page, final_movies, repo: AbstractRepository):
    movies_selected_in_right_form = list()
    for movie in final_movies:
        movie_in_right_form = repo.get_movie_by_rank(movie['rank'])
        movies_selected_in_right_form.append(movie_in_right_form)
    movies_selected = movies_selected_in_right_form[cursor:cursor + movies_per_page]
    movies_as_dict = movies_to_dict(movies_selected)
    return movies_as_dict


def get_all_movies_by_genre(genre, repo: AbstractRepository):
    movies = repo.get_movies_by_genre(genre)
    # print(len(movies))
    if movies is None:
        raise NonExistentMovieException
    return movies_to_dict(movies)


def get_movies_by_director(director, repo: AbstractRepository):
    # Returns movies by the particular director
    movies = repo.get_movies_by_director(director)
    if movies is None:
        raise NonExistentMovieException
    return movies_to_dict(movies)


def get_movies_by_actor(actor, repo: AbstractRepository):
    # Returns movies with the particular actor
    movies = repo.get_movies_by_actor(actor)
    if movies is None:
        raise NonExistentMovieException
    return movies_to_dict(movies)


def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'title': movie.title,
        'year': movie.release_year(),
        'genres': movie.genres,
        'actors': movie.actors,
        'director': movie.director,
        'description': movie.description,
        'reviews': reviews_to_dict(movie.reviews),
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.username,
        'movie': review.movie.title,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]
