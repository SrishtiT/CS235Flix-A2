from cs235flix.datafilereaders.MovieFileCSVReader import MovieFileCSVReader
import os


def test_dataset_lengths():
    data_path = os.path.join('C:', os.sep, 'Users', 'Sanjeev Toora', 'Desktop', 'Srishti new',
                             'srishti-cs230', 'CS235FlixSkeleton-Extensions', 'data', 'Data1000Movies.csv')
    movie_file_reader = MovieFileCSVReader(data_path)
    movie_file_reader.read_csv_file()
    length_movies = len(movie_file_reader._dataset_of_movies)
    length_actors = len(movie_file_reader._dataset_of_actors_and_movies.keys())
    length_directors = len(movie_file_reader._dataset_of_directors_and_movies.keys())
    length_genres = len(movie_file_reader._dataset_of_genres_and_movies.keys())
    assert length_movies == 1000
    assert length_actors == 1985
    assert length_directors == 644
    assert length_genres == 20
    first_movie_rank = movie_file_reader._dataset_of_movies[1].rank
    first_movie_genres = movie_file_reader._dataset_of_movies[1].genres
    first_movie_actors = movie_file_reader._dataset_of_movies[1].actors
    first_movie_director = movie_file_reader._dataset_of_movies[1].director
    assert first_movie_rank == 1
    assert len(first_movie_genres) == 3
    assert len(first_movie_actors) == 4
    assert first_movie_director == 'James Gunn'




