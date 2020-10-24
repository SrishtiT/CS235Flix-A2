import pytest

import cs235flix.utilities.services as services
from cs235flix.movies import services as movies_services
from cs235flix.authentication.services import AuthenticationException
from cs235flix.authentication import services as auth_services


def test_can_add_user(memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, memory_repo)

    user_as_dict = auth_services.get_user(new_username, memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, memory_repo)


def test_authentication_with_valid_credentials(memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', memory_repo)


def test_can_add_review(memory_repo):
    username = 'fmercury'
    review_text = 'Left me in stitches!!'
    rating = 9
    rank = 8
    # Call the service layer to add the review.
    movies_services.add_review(rank, username,  review_text, rating, memory_repo)

    # Retrieve the reviews for the movie from the repository.
    reviews_as_dict = movies_services.get_reviews_for_movie(rank, memory_repo)

    # Check that the reviews include a comment with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(memory_repo):
    rank = 1001
    username = 'fmercury'
    review_text = 'Fun family movie!!'
    rating = 9

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(rank, username, review_text, rating, memory_repo)


def test_cannot_add_review_by_unknown_user(memory_repo):
    rank = 8
    username = 'Chlorexx'
    review_text = 'Left me in stitches!!'
    rating = 9

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(rank, username, review_text, rating, memory_repo)


def test_can_get_movie_by_title(memory_repo):
    title = "Sing"

    movie_as_dict = movies_services.get_movie(title, memory_repo)
    assert movie_as_dict['title'] == "Sing"
    assert movie_as_dict['year'] == 2016


def test_cannot_get_non_existent_movie_by_title(memory_repo):
    title = "Moana2"

    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(title, memory_repo)


def test_can_get_movie_by_genre(memory_repo):
    genre = "Comedy"
    movies_as_dict = movies_services.get_all_movies_by_genre(genre, memory_repo)
    assert len(movies_as_dict) == 3


def test_cannot_get_non_existent_movie_by_genre(memory_repo):
    genre = "Comedy-Horror"
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_all_movies_by_genre(genre, memory_repo)


def test_can_get_movie_by_director(memory_repo):
    director = "Christophe Lourdelet"
    movies_as_dict = movies_services.get_movies_by_director(director, memory_repo)
    assert len(movies_as_dict) == 1


def test_cannot_get_non_existent_movie_by_director(memory_repo):
    director = "Joy Cowley"
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movies_by_director(director, memory_repo)


def test_can_get_movie_by_actor(memory_repo):
    actor = "Chris Pratt"
    movies_as_dict = movies_services.get_movies_by_actor(actor, memory_repo)
    assert len(movies_as_dict) == 2


def test_cannot_get_non_existent_movie_by_actor(memory_repo):
    actor = "Luke Skywalker"
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movies_by_actor(actor, memory_repo)


def test_get_reviews(memory_repo):
    rank = 4
    reviews_as_dict = movies_services.get_reviews_for_movie(4, memory_repo)

    # Check that 1 review was returned for the movie titled 'Sing'
    assert len(reviews_as_dict) == 1


def test_get_reviews_for_non_existent_movie(memory_repo):
    with pytest.raises(movies_services.NonExistentMovieException):
        reviews_as_dict = movies_services.get_reviews_for_movie(1001, memory_repo)


def test_get_reviews_for_movie_without_reviews(memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(1, memory_repo)
    assert len(reviews_as_dict) == 0
