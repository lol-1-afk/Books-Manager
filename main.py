import sqlite3

from misc import Models
from misc.DataBase import DataBase

# init DataBase class
__conn__ = sqlite3.connect("db.db", check_same_thread=False)
__conn__.row_factory = sqlite3.Row
database = DataBase(__conn__)


def validate_input(variations: str, allowed_actions: list[int]) -> int:
    """
    Validates user's input not get unhandled errors

    :param variations: string with list of actions
    :param allowed_actions: list of allowed actions
    :return: user's selected action
    """
    variations = f"{'-' * 32}\n0 - выход\n" + variations

    print(variations)

    while True:
        users_choice = input("Выберите действие: ")

        try:  # check if input is digit
            users_choice = int(users_choice)
        except ValueError:
            print("Пожалуйста, введите цирфу!")
            continue

        if users_choice == 0:  # exit if 0
            print("Досвидания")
            quit(-1)

        if users_choice not in allowed_actions:  # allowed action
            print("Ваш выбор вне списка допустимых вариантов")
            continue

        print("-" * 32)
        return users_choice


def get_info() -> tuple:
    """
    Asks user for basic book information and returns it

    :return: tuple(book_name, book_author, book_year)
    """

    book_name = input("Название книги: ")
    book_author = input("Автор книги: ")
    book_year = input("Год публикации книги: ")
    return book_name, book_author, book_year


def show_books(books: list[Models.Book] or Models.Book):
    """
    Shows info about each book in list (or about single book)

    :param books:  list of books to show / single book var
    :return: None
    """

    if isinstance(books, Models.Book):  # single book, not list
        books = [books]

    for book in books:
        print(
            f"--------------------------\n"
            f"ID: {book.id}\n"
            f"Название: {book.name}\n"
            f"Автор: {book.author}\n"
            f"Год издания: {book.year}"
        )


def add_book():
    """
    Adds book to database

    :return: None
    """

    book_name, book_author, book_year = get_info()

    # validate inputs
    if not book_name or not book_author or not book_year.isdigit() or int(book_year) < 0:
        print("Вы ввели что-то не то")
        return

    database.add_book(
        name=book_name,
        author=book_author,
        year=int(book_year)
    )
    print("Книга успешно добавлена в базу")


def search_books():
    """
    Searchs for books and shows results

    :return: None
    """

    print("Введите известные данные о книге. Если вы не знаете, ничего не пишите")
    book_name, book_author, book_year = get_info()

    if not book_name and not book_author and not book_year:
        print("Пожалуйста, укажите одно и более значение")
        return

    show_books(database.search_books(
        name=book_name,
        author=book_author,
        year=book_year
    ))


def delete_book():
    """
    Delets book from database

    :return: None
    """

    book_id = input("Уникальный числовой идентификатор книги (ID): ")

    if not book_id.isdigit():
        print("Вы ввели что-то не то")
        return

    database.delete_book(book_id=int(book_id))
    print("Если такая книга существовала, то теперь её нет")


def edit_book_info():
    """
    Edits information about book by id

    :return: None
    """
    book_id = input("Уникальный числовой идентификатор книги (ID): ")

    if not book_id.isdigit():
        print("Вы ввели что-то не то")
        return

    book_name, book_author, book_year = get_info()

    if not book_name and not book_author and not book_year:
        print("Вы ввели что-то не то")
        return

    arguments = {}
    if book_name:
        arguments["name"] = book_name
    if book_author:
        arguments["author"] = book_author
    if book_year:
        arguments["year"] = book_year

    show_books(database.edit_book(
        book_id=int(book_id),
        **arguments
    ))


def list_books():
    """
    Shows information about all books in database

    :return: None
    """

    show_books(database.get_all_books())


def main():
    """
    Main function to select action

    :return: None
    """
    functionality = {
        1: add_book,
        2: search_books,
        3: delete_book,
        4: edit_book_info,
        5: list_books
    }

    while True:
        action = validate_input(
            variations="1 - добавить книгу\n"
                       "2 - найти книги\n"
                       "3 - удалить книгу\n"
                       "4 - изменить инфонрмацию о книге\n"
                       "5 - список всех книг",
            allowed_actions=[1, 2, 3, 4, 5]
        )

        functionality[action]()


if __name__ == "__main__":
    main()
