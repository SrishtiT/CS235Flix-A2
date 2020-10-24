import pytest

from cs235flix.domainmodel.model import Movie, User, Review


def test_init():
    movie = Movie(14, "Moana", 2016, ["Animation", "Adventure", "Comedy"],
                  ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
                  'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    assert repr(movie) == "<Movie Moana, 2016>"
    assert movie.rank == 14
    assert movie.genres == ["Animation", "Adventure", "Comedy"]
    assert movie.actors == ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"]
    assert movie.director == "Ron Clements"
    assert movie.description == "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right."


def test_runtime_minutes():
    movie = Movie(14, "Moana", 2016, ["Animation", "Adventure", "Comedy"],
                  ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
                  'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    movie.runtime_minutes = 120
    assert movie.runtime_minutes == 120


def test_runtime_minutes_neg():
    movie = Movie(14, "Moana", 2016, ["Animation", "Adventure", "Comedy"],
                  ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
                  'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    with pytest.raises(ValueError):
        movie.runtime_minutes = -20


def test_hash():
    a_set = set()
    movie = Movie(14, "Moana", 2016, ["Animation", "Adventure", "Comedy"],
                  ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
                  'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    a_set.add(movie)
    a_set.add(movie)
    assert len(a_set) == 1


def test_normal_user():
    user1 = User('Martin', 'pw12345')
    assert repr(user1) == "<User Martin>"
    movie = Movie(14, "Moana", 2016, ["Animation", "Adventure", "Comedy"],
                  ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
                  'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    movie.runtime_minutes = 107
    user1.watch_movie(movie)
    assert len(user1._watched_movies) == 1
    assert user1.time_spent_watching_movies_minutes == 107


def test_normal_review():
    user = User("Sarah", "abcdefgh")
    movie = Movie(14, "Moana", 2016, ["Animation", "Adventure", "Comedy"],
                  ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
                  'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    review_text = "This movie was very enjoyable."
    rating = 10
    review = Review(user, movie, review_text, rating)
    assert repr(review.user) == "<User Sarah>"
    assert repr(review.movie) == "<Movie Moana, 2016>"
    assert review.review_text == "This movie was very enjoyable."
    assert review.rating == 10


def test_negative_rating():
    user = User("Sarah", "abcdefgh")
    movie = Movie(14,"Moana", 2016,["Animation","Adventure","Comedy"],
            ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
            'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    review_text = "This movie was very enjoyable."
    rating = -10
    review = Review(user, movie, review_text, rating)
    assert review.rating is None


def test_extreme_rating():
    user = User("Sarah", "abcdefgh")
    movie = Movie(14,"Moana", 2016,["Animation","Adventure","Comedy"],
            ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
            'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    review_text = "This movie was very enjoyable."
    rating = 100
    review = Review(user, movie, review_text, rating)
    assert review.rating is None


def test_string_rating():
    user = User("Sarah", "abcdefgh")
    movie = Movie(14,"Moana", 2016,["Animation","Adventure","Comedy"],
            ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
            'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    review_text = "This movie was very enjoyable."
    rating = "a"
    review = Review(user, movie, review_text, rating)
    assert review.rating is None


def test_int_review():
    user = User("Sarah", "abcdefgh")
    movie = Movie(14,"Moana", 2016,["Animation","Adventure","Comedy"],
            ["Auli'i Cravalho", "Dwayne Johnson", "Rachel House", "Temuera Morrison"],
            'Ron Clements', "In Ancient Polynesia, when a terrible curse incurred by the \
            Demigod Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's ' \
            call to seek out the Demigod to set things right.")
    review_text = 5
    rating = 10
    review = Review(user, movie, review_text, rating)
    assert review.review_text is None
