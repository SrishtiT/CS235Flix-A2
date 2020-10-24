from cs235flix.adapters.repository import AbstractRepository


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre for genre in genres]
    return genre_names
