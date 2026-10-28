import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

class Displayer(ABC):
    @abstractmethod
    def display(self, book: Book) -> None:
        pass


class ConsoleDisplayer(Displayer):
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplayer(Displayer):
    def display(self, book: Book) -> None:
        print(book.content[::-1])


class Printer(ABC):
    @abstractmethod
    def print_book(self, book: Book) -> None:
        pass


class ConsolePrinter(Printer):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrinter(Printer):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class Serializer(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


class BookService:
    def __init__(self) -> None:
        self.displayers = {
            "console": ConsoleDisplayer(),
            "reverse": ReverseDisplayer(),
        }
        self.printers = {
            "console": ConsolePrinter(),
            "reverse": ReversePrinter(),
        }
        self.serializers = {
            "json": JsonSerializer(),
            "xml": XmlSerializer(),
        }

    def execute(self, book: Book, commands: list[tuple[str, str]]) -> None | str:
        for command, method_type in commands:
            if command == "display":
                self._run(self.displayers, method_type, "display", book)
            elif command == "print":
                self._run(self.printers, method_type, "print_book", book)
            elif command == "serialize":
                return self._run(
                    self.serializers, method_type, "serialize", book
                )

    @staticmethod
    def _run(handlers: dict, key: str, method: str, book: Book) -> None | str:
        try:
            handler = handlers[key]
        except KeyError as error:
            raise ValueError(f"Unknown {method} type: {key}") from error
        return getattr(handler, method)(book)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    return BookService().execute(book, commands)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
