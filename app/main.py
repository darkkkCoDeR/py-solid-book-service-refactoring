from app.book import Book
from app.book_service import BookService


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    return BookService().execute(book, commands)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
