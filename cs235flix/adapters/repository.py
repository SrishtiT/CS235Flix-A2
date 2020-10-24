import abc

from typing import List

from cs235flix.domainmodel.model import User, Movie

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_movies(self):
        """ Returns the movies stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self):
        """ Returns the genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors(self):
        """ Returns the directors stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self):
        """ Returns the actors stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title):
        """ Returns the Movies with the given title from the repository

        If there is no Movie with the given title, this method returns None.
        """
        raise NotImplementedError

    def get_movie_by_rank(self, rank):
        """ Returns the Movie with the given rank from the repository

        If there is no Movie with the given rank, this method returns None.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre) -> List[Movie]:
        """ Returns the Movies from the given genre from the repository

        If there is no Movie from the given genre, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director) -> List[Movie]:
        """ Returns the Movies from the given director from the repository

        If there is no Movie from the given director, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor) -> List[Movie]:
        """ Returns the Movies from the given actor from the repository

        If there is no Movie from the given actor, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a user to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    #delete once done
    def get_users(self) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    def add_review(self, review):
        """ Adds a Review to the repository.

        If the Comment doesn't have bidirectional links with an Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """

        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Comment not correctly attached to a movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError


