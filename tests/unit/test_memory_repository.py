import pytest
from cs235flix.domainmodel.model import User, Movie, make_review, Review
from cs235flix.adapters.repository import RepositoryException


def test_repository_records_and_retrieves_all_movies(memory_repo):
    assert memory_repo.get_number_of_movies() == 10
    assert len(memory_repo.get_movies()) == 10


def test_repository_records_and_retrieves_all_genres(memory_repo):
    # There are 14 different genres in the first 10 lines of the movies CSV file.
    assert len(memory_repo.get_genres()) == 14


def test_repository_records_and_retrieves_all_directors(memory_repo):
    # There are 10 different actors in the first 10 lines of the movies CSV file.
    assert len(memory_repo.get_directors()) == 10


def test_repository_records_and_retrieves_all_actors(memory_repo):
    # There are 39 different genres in the first 10 lines of the movies CSV file.
    assert len(memory_repo.get_actors()) == 39


def test_get_movie_if_movie_in_dict(memory_repo):
    movie = memory_repo.get_movie("Split")
    assert type(movie) is Movie
    assert movie.title == "Split"


def test_get_movie_if_movie_not_in_dict(memory_repo):
    # Lion not in the first 10 lines of the movies CSV file.
    movie = memory_repo.get_movie("Lion")
    assert movie is None


def test_get_movies_by_genre_if_genre_in_dict(memory_repo):
    movies_list = memory_repo.get_movies_by_genre("Action")
    assert len(movies_list) == 4


def test_get_movie_by_rank(memory_repo):
    movie = memory_repo.get_movie_by_rank(1)
    assert movie.title == "Guardians of the Galaxy"


def test_get_movies_by_genre_if_genre_not_in_dict(memory_repo):
    # no Western movie in the first 10 lines of the movies CSV file.
    movies_list = memory_repo.get_movies_by_genre("Western")
    assert movies_list is None


def test_get_movies_by_director_if_director_in_dict(memory_repo):
    movies_list = memory_repo.get_movies_by_director("M. Night Shyamalan")
    assert len(movies_list) == 1


def test_get_movies_by_director_if_director_not_in_dict(memory_repo):
    # Gareth Edwards did not direct one of movies in the first 10 lines of the movies CSV file.
    movies_list = memory_repo.get_movies_by_genre("Gareth Edwards")
    assert movies_list is None


def test_get_movies_by_actor_if_actor_in_dict(memory_repo):
    movies_list = memory_repo.get_movies_by_actor("Chris Pratt")
    assert len(movies_list) == 2


def test_get_movies_by_actor_if_actor_not_in_dict(memory_repo):
    # Dev Patel did not act in one of movies in the first 10 lines of the movies CSV file.
    movies_list = memory_repo.get_movies_by_actor("Dev Patel")
    assert movies_list is None


def test_repository_can_add_a_user(memory_repo):
    user = User('Sarah', '123456789')
    memory_repo.add_user(user)
    assert memory_repo.get_num_of_users() == 4


def test_repository_can_get_a_user(memory_repo):
    user = User('Dave', '123456789')
    memory_repo.add_user(user)
    # Note that User's __init__() method use to convert the name to lower case.
    assert type(memory_repo.get_user('Dave')) is User


def test_repository_does_not_retrieve_a_non_existent_user(memory_repo):
    user = memory_repo.get_user('prince')
    assert user is None


def test_repository_can_add_a_review(memory_repo):
    user = memory_repo.get_user('thorke')
    movie = memory_repo.get_movie("Split")
    review = make_review(user, movie, "Scary stuff!", 7)

    memory_repo.add_review(review)
    assert review in memory_repo.get_reviews()
    assert review.user.username == "thorke"
    assert review.movie.title == "Split"
    assert review.review_text == "Scary stuff!"
    assert review.rating == 7
    assert len(memory_repo.get_reviews()) == 3


def test_repository_does_not_add_a_review_without_a_user(memory_repo):
    movie = memory_repo.get_movie("Split")
    review = Review(None, movie, "Scary stuff!", 7)

    with pytest.raises(RepositoryException):
        memory_repo.add_review(review)
    assert len(memory_repo.get_reviews()) == 2


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(memory_repo):
    user = memory_repo.get_user('thorke')
    movie = memory_repo.get_movie("Split")
    review = Review(None, movie, "Scary stuff!", 7)

    user.add_review(review)
    with pytest.raises(RepositoryException):
        # Exception expected because the Movie doesn't refer to the review.
        memory_repo.add_review(review)
    assert len(memory_repo.get_reviews()) == 2


def test_repository_can_retrieve_reviews(memory_repo):
    assert len(memory_repo.get_reviews()) == 2
