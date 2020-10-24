import csv
import os

from werkzeug.security import generate_password_hash

from cs235flix.adapters.repository import AbstractRepository

from cs235flix.domainmodel.model import Movie, User, Review, make_review

from cs235flix.datafilereaders.MovieFileCSVReader import MovieFileCSVReader

DATA_PATH = os.path.join('C:', os.sep, 'Users', 'Sanjeev Toora', 'Desktop', 'Srishti new',
                         'srishti-cs230', 'CS235FlixSkeleton-Extensions', 'data')


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._users = list()
        self._movies = dict()
        self._actors_and_movies = dict()
        self._genres_and_movies = dict()
        self._directors_and_movies = dict()
        self._reviews = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username):
        for user in self._users:
            if user.username == username:
                return user
        return None

    # delete once done
    def get_users(self):
        return self._users

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def get_number_of_movies(self):
        return len(self._movies)

    def get_movies(self):
        return list(self._movies.values())

    def get_genres(self):
        genres = list(self._genres_and_movies.keys())
        return genres

    def get_directors(self):
        directors = list(self._directors_and_movies.keys())
        return directors

    def get_actors(self):
        actors = list(self._actors_and_movies.keys())
        return actors

    def get_movie(self, title):
        for movie in self._movies.values():
            if movie.title == title:
                return movie
        return None

    def get_movie_by_rank(self, rank):
        rank = int(rank)
        if 0 < rank < 1001:
            return self._movies[rank]
        return None

    def get_movies_by_genre(self, genre):
        if genre in self._genres_and_movies.keys():
            return self._genres_and_movies[genre]
        return None

    def get_movies_by_director(self, director):
        if director in self._directors_and_movies.keys():
            return self._directors_and_movies[director]
        return None

    def get_movies_by_actor(self, actor):
        if actor in self._actors_and_movies.keys():
            return self._actors_and_movies[actor]
        return None

    def get_num_of_users(self):
        return len(self._users)

    def populate(self, num_of_rows="ALL"):
        reader = MovieFileCSVReader(os.path.join(DATA_PATH, 'Data1000Movies.csv'))
        if num_of_rows == "ALL":
            reader.read_csv_file()
        else:
            reader.read_csv_file(num_of_rows)
        self._movies = reader.dataset_of_movies
        self._actors_and_movies = reader.dataset_of_actors_and_movies
        self._genres_and_movies = reader.dataset_of_genres_and_movies
        self._directors_and_movies = reader.dataset_of_directors_and_movies
        if num_of_rows != "ALL":
            data_path_users = os.path.join(DATA_PATH, 'users.csv')
            data_path_reviews = os.path.join(DATA_PATH, 'reviews.csv')
            for data_row in read_csv_file(data_path_users):
                user = User(
                    username=data_row[0],
                    password=generate_password_hash(data_row[1])
                )
                self._users.append(user)
            for data_row in read_csv_file(data_path_reviews):
                review = make_review(
                    user=self.get_user(data_row[0]),
                    movie=self.get_movie(data_row[1]),
                    review_text=data_row[2],
                    rating=int(data_row[3])
                )
                self._reviews.append(review)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row
