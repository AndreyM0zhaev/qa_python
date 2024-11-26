from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()


def test_add_new_book_creates_entry(collector):
    collector.add_new_book('1984')
    assert '1984' in collector.get_books_genre()


def test_add_new_book_no_empty_name(collector):
    collector.add_new_book('')
    assert collector.get_books_genre() == {}


def test_add_new_book_length_limit(collector):
    collector.add_new_book('a' * 41)
    assert collector.get_books_genre() == {}


@pytest.mark.parametrize("book_name", [
    ('Книга 1'),
    ('Книга 2'),
    ('Книга 3')
])
def test_add_new_book_multiple(collector, book_name):
    collector.add_new_book(book_name)
    assert book_name in collector.get_books_genre()


def test_set_book_genre_updates_genre(collector):
    collector.add_new_book('1984')
    collector.set_book_genre('1984', 'Фантастика')
    assert collector.get_book_genre('1984') == 'Фантастика'


def test_set_book_genre_not_in_collection(collector):
    collector.set_book_genre('Неизвестная Книга', 'Фантастика')
    assert collector.get_books_genre() == {}


def test_get_book_genre_returns_correct_genre(collector):
    collector.add_new_book('1984')
    collector.set_book_genre('1984', 'Фантастика')
    assert collector.get_book_genre('1984') == 'Фантастика'


def test_get_books_with_specific_genre(collector):
    collector.add_new_book('1984')
    collector.set_book_genre('1984', 'Фантастика')
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')

    assert collector.get_books_with_specific_genre('Фантастика') == ['1984']
    assert collector.get_books_with_specific_genre('Ужасы') == ['Оно']
    assert collector.get_books_with_specific_genre('Комедии') == []


@pytest.mark.parametrize("genres", [
    ('Ужасы'),
    ('Детективы')
])
def test_get_books_for_children_excludes_genres(collector, genres):
    collector.add_new_book('Книга 1')
    collector.set_book_genre('Книга 1', genres)
    collector.add_new_book('Книга 2')
    collector.set_book_genre('Книга 2', 'Фантастика')

    assert 'Книга 1' not in collector.get_books_for_children()
    assert 'Книга 2' in collector.get_books_for_children()


def test_get_books_for_children_includes_non_restricted_genres(collector):
    collector.add_new_book('Книга 1')
    collector.set_book_genre('Книга 1', 'Фантастика')

    assert collector.get_books_for_children() == ['Книга 1']

def test_add_book_in_favorites(collector):
    collector.add_new_book("Harry Potter")
    collector.add_book_in_favorites("Harry Potter")
    assert "Harry Potter" in collector.favorites


def test_add_book_in_favorites_not_existing(collector):
    collector.add_book_in_favorites("Не существующая книга")
    assert "Не существующая книга" not in collector.favorites


def test_delete_book_from_favorites(collector):
    collector.add_new_book("Harry Potter")
    collector.add_book_in_favorites("Harry Potter")
    collector.delete_book_from_favorites("Harry Potter")
    assert "Harry Potter" not in collector.favorites


def test_get_list_of_favorites_books(collector):
    collector.add_new_book("Harry Potter")
    collector.add_book_in_favorites("Harry Potter")
    favorite_books = collector.get_list_of_favorites_books()
    assert favorite_books == ["Harry Potter"]