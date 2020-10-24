from cs235flix.adapters.memory_repository import MemoryRepository
import cs235flix.utilities.services as services

def test_get_genre_and_urls():
    repo = MemoryRepository()
    repo.populate()
    genre_names = services.get_genre_names(repo)
