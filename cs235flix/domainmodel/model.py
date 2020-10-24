from datetime import datetime
from typing import Iterable, List


class Movie:

    def __init__(self, rank: int, title: str, release_year: int, genres, actors, director, description):
        self._reviews: List[Review] = list()
        if type(rank) is int and 0 < rank < 1001:
            self._rank = rank
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()
        if release_year >= 1990:
            self._release_year = release_year
        else:
            self._release_year = None
        self._director = director
        self._actors = actors
        self._genres = genres
        self._description = description
        self._runtime_minutes: int = None

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def title(self) -> str:
        return self._title

    @property
    def actors(self):
        return self._actors

    @property
    def genres(self):
        return self._genres

    @property
    def description(self):
        return self._description

    @property
    def director(self):
        return self._director

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    def release_year(self):
        return self._release_year

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self._reviews)

    @property
    def number_of_reviews(self) -> int:
        return len(self._reviews)

    @description.setter
    def description(self, description):
        self._description = description.strip()

    @director.setter
    def director(self, director):
        self._director = director

    @runtime_minutes.setter
    def runtime_minutes(self, minutes):
        if minutes > 0:
            self._runtime_minutes = minutes
        else:
            raise ValueError()

    def add_actor(self, actor):
        self._actors.append(actor)

    def add_genre(self, genre):
        self._genres.append(genre)

    def remove_actor(self, actor):
        if actor in self._actors:
            self._actors.remove(actor)

    def remove_genre(self, genre):
        if genre in self._genres:
            self._genres.remove(genre)

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    def __repr__(self):
        return f"<Movie {self._title}, {self._release_year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return (
                other._title == self._title and
                other._release_year == self._release_year
        )

    def __get_unique_string_rep(self):
        return f"{self._title}, {self._release_year}"

    def __lt__(self, other):
        return self.__get_unique_string_rep() < other.__get_unique_string_rep()

    def __hash__(self):
        return hash(self.__get_unique_string_rep())


class User:
    def __init__(self, username: str, password: str):
        if username == "" or type(username) is not str:
            self._username = None
        else:
            self._username = username.strip()
        self._password = password
        self._watched_movies = list()
        self._reviews = list()
        self._time_spent_watching_movies_minutes: int = 0
        self._watchlist = list()

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    @property
    def watchlist(self):
        return self._watchlist

    def watch_movie(self, movie: Movie):
        self._watched_movies.append(movie)
        self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    def add_movie_to_watchlist(self, movie: Movie):
        self._watchlist.append(movie)

    def remove_movie_from_watch_list(self, movie: Movie):
        self._watchlist.remove(movie)

    def __repr__(self):
        return f"<User {self._username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
                other._username == self._username
        )

    def __lt__(self, other):
        return self._username < other._username

    def __hash__(self):
        return hash(self._username)


class Review:
    def __init__(self, user: User, movie: Movie, review_text: str, rating: int):
        self._user = user
        self._movie: Movie = movie
        if review_text == "" or type(review_text) is not str:
            self._review_text = None
        else:
            self._review_text = review_text
        if type(rating) is not int:
            self._rating = None
        elif rating > 10 or rating < 1:
            self._rating = None
        else:
            self._rating = rating
        self._timestamp = datetime.today()

    @property
    def user(self) -> User:
        return self._user

    @property
    def movie(self):
        return self._movie

    @property
    def review_text(self):
        return self._review_text

    @property
    def rating(self):
        return self._rating

    @property
    def timestamp(self):
        return self._timestamp

    def __repr__(self):
        return f"<User: {self._user} \nMovie {self._movie}> \nReview: {self._review_text} \nRating:" \
               f" {self._rating} \nTimestamp: {self._timestamp}"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return (
                other._user == self._user and
                other._movie == self._movie and
                other._review_text == self._review_text and
                other._rating == self._rating and
                other._timestamp == self._timestamp
        )


class ModelException(Exception):
    pass


def make_review(user: User, movie: Movie, review_text: str, rating: int):
    if user is not None and movie is not None:
        review = Review(user, movie, review_text, rating)
        user.add_review(review)
        movie.add_review(review)
        return review
