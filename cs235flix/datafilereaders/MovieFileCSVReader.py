from cs235flix.domainmodel.model import Movie
import csv


class MovieFileCSVReader:
    def __init__(self, file_name: str):
        if file_name == "" or type(file_name) is not str:
            self._file_name = None
        else:
            self._file_name = file_name
        self._dataset_of_movies = dict()
        self._dataset_of_genres_and_movies = dict()
        self._dataset_of_actors_and_movies = dict()
        self._dataset_of_directors_and_movies = dict()

    @property
    def dataset_of_movies(self):
        return self._dataset_of_movies

    @property
    def dataset_of_actors_and_movies(self):
        return self._dataset_of_actors_and_movies

    @property
    def dataset_of_directors_and_movies(self):
        return self._dataset_of_directors_and_movies

    @property
    def dataset_of_genres_and_movies(self):
        return self._dataset_of_genres_and_movies

    def read_csv_file(self, num_of_rows="ALL"):
        input_file = csv.DictReader(open(self._file_name, encoding="utf-8-sig"))
        count = 0
        for row in input_file:
            each_movie_genres_stripped = list()
            each_movie_actors_stripped = list()
            each_movie_genres = row["Genre"].split(",")
            for genre in each_movie_genres:
                genre = genre.strip()
                each_movie_genres_stripped.append(genre)
            each_movie_actors = row["Actors"].split(",")
            for actor in each_movie_actors:
                actor = actor.strip()
                each_movie_actors_stripped.append(actor)
            director = row["Director"].strip()
            description = row["Description"].strip()
            rank = int(row["Rank"])
            movie = Movie(rank, row["Title"], int(row["Year"]), each_movie_genres_stripped, each_movie_actors_stripped,
                          director, description)

            # rank (movies list)
            self._dataset_of_movies[rank] = movie
            # genre and movies list
            for genre in each_movie_genres:
                genre = genre.strip()
                if genre not in self._dataset_of_genres_and_movies.keys():
                    self._dataset_of_genres_and_movies[genre] = [movie]
                else:
                    self._dataset_of_genres_and_movies[genre].append(movie)
            # actors and movies list
            each_movie_actors = row["Actors"].split(",")
            for actor in each_movie_actors:
                actor = actor.strip()
                if actor not in self._dataset_of_actors_and_movies.keys():
                    self._dataset_of_actors_and_movies[actor] = [movie]
                else:
                    self._dataset_of_actors_and_movies[actor].append(movie)
            # director and movies list
            if director not in self._dataset_of_directors_and_movies.keys():
                self._dataset_of_directors_and_movies[director] = [movie]
            else:
                self._dataset_of_directors_and_movies[director].append(movie)
            count += 1
            if num_of_rows != "ALL":
                if count == num_of_rows:
                    break
