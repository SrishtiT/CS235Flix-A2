import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test',
         b'Your password must at least 8 characters, and contain an upper case letter, '
         b'a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235FLIX' in response.data


def test_login_required_to_review(client):
    response = client.post('/review_movie')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('review_movie?rank=1&cursor=0&genre=Adventure')

    response = client.post(
        '/review_movie',
        data={'review': 'Great family movie',
              'rating': 9,
              'rank': 1,
              'genre': 'Adventure',
              'cursor': 0}
    )
    assert response.headers[
               'Location'] == 'http://localhost/movies_by_genre?genre=Adventure&view_reviews_for=1&cursor=0'


@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks Trump is a fucking good movie?', (b'Your review must not contain profanity')),
        ('Meh', (b'Your review is too short')),
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to review a movie.
    response = client.post(
        '/comment',
        data={'review': 'review',
              'rating': 9,
              'rank': 1,
              'genre': 'Adventure',
              'cursor': 0}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movie_with_review(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Animation&view_reviews_for=4&cursor=0')
    assert response.status_code == 200

    # Check that all reviews for specified movie are included on the page.
    assert b'Great family movie' in response.data


def test_movies_by_genre(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Action')
    assert response.status_code == 200

    # Check that all movies of certain genre are included on the page.
    assert b'Action Movies' in response.data
    assert b'Guardians of the Galaxy' in response.data
    assert b'Suicide Squad' in response.data
    assert b'The Great Wall' in response.data
    assert b'The Lost City of Z' in response.data


def test_movies_by_searching_actor(client):
    # Check that we can retrieve the movies page.
    response = client.get('search_results?actor=Chris+Pratt&genre=&director=')
    assert response.status_code == 200

    # Check that all movies including certain actor are included on the page.
    assert b'Guardians of the Galaxy' in response.data


def test_movies_by_searching_genre(client):
    # Check that we can retrieve the movies page.
    response = client.get('search_results?actor=&genre=Romance&director=')
    assert response.status_code == 200

    # Check that all movies of certain genre are included on the page.
    assert b'Passengers' in response.data


def test_movies_by_searching_director(client):
    # Check that we can retrieve the movies page.
    response = client.get('/search_results?actor=&genre=&director=Ridley+Scott')
    assert response.status_code == 200

    # Check that all movies by certain director are included on the page.
    assert b'Prometheus' in response.data


def test_movies_by_combination_searching_valid(client):
    # Check that we can retrieve the movies page.
    response = client.get('/search_results?actor=James+McAvoy&genre=Horror&director=')
    assert response.status_code == 200

    # Check that all movies by certain director are included on the page.
    assert b'Split' in response.data


def test_movies_by_combination_searching_invalid(client):
    # Check that we can retrieve the movies page.
    response = client.get('/search_results?actor=James+McAvoy&genre=Music&director=')
    assert response.status_code == 200

    # Check that all movies by certain director are included on the page.
    assert b'No Movies Found' in response.data
