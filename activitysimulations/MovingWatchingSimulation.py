from cs235flix.domainmodel.model import Movie, Review, User, Review
from typing import List


class MovieWatchingSimulation:

    def __init__(self, movie_watched: Movie):
        if type(movie_watched) is Movie:
            self._movie_watched_together: Movie = movie_watched
        else:
            raise TypeError()
        self._reviews: List[Review] = []
        self._users: List[User] = []

    @property
    def movie_watched_together(self):
        return self._movie_watched_together

    @property
    def reviews(self):
        return self._reviews

    @property
    def users(self):
        return self._users

    def create_and_add_review_movie_and_user_to_group_and_individual_list(self, user: User, review_text: str, rating: int):
        if type(user) is not User or type(review_text) is not str or type(rating) is not int:
            raise TypeError()
        else:
            self._users.append(user)
            review = Review(user, self._movie_watched_together, review_text, rating)
            self._reviews.append(review)
            user.watch_movie(self._movie_watched_together)
            user.add_review(review)

    def __repr__(self):
        review_str = ""
        for i in range(len(self._users)):
            review_str += repr(self._users[i]) + "\n" + repr(self._reviews[i]) + "\n"
        return f"CS235Flix Party Reviews: \n{review_str}>"
