import sqlite3

from misc import Models


class DataBase:
    def __init__(self, connection: sqlite3.Connection):
        self.__db = connection
        self.__cur = connection.cursor()
        self.__cur.execute(
            '''CREATE TABLE IF NOT EXISTS "books" (
                "id" INTEGER,
                "name"	TEXT,
                "author"    TEXT,
                "year"  INTEGER,
                PRIMARY KEY("id")
            )'''
        )

    def add_book(self, name: str, author: str, year: int) -> Models.Book:
        """
        - Добавление книги: Пользователь вводит информацию о книге: название, автор, год издания.
        Данные сохраняются в базу.

        Adds a new book to database

        :param name: book's name
        :param author: book's author
        :param year: year when book was published
        :return: New instance of Models.Book with given data
        """

        last_book_id = self.__cur.execute("SELECT id FROM books ORDER BY id DESC LIMIT 1").fetchone()  # get last id
        if not last_book_id:  # empy database, id = 1
            new_id = 1
        else:
            new_id = last_book_id[0] + 1  # last book's id + 1

        query = "INSERT INTO books (id, name, author, year) VALUES (?, ?, ?, ?)"
        self.__cur.execute(query, (new_id, name, author, year))
        self.__db.commit()

        return Models.Book(new_id, name, author, year)

    def search_books(self, name: str = None, author: str = None, year: int or str = None) -> list[Models.Book] or []:
        """
        - Поиск книги: По заданным параметрам (название, автор, год издания) производится поиск
        соответствующих книг в базе.

        Searchs for all books that match query

        :param name: keyword that book's name must contain
        :param author: author of book
        :param year: year of book's publications
        :raises ValueError if bad query given
        :return: list of [Models.Book] or empty list
        """

        if not name and not author and not year:
            raise ValueError("Bad searching query was given. can't find anything. Pass some information about book")

        query = "SELECT id, name, author, year FROM books WHERE 1"
        query_params = []

        # conditions
        if name:
            query += " AND name LIKE ?"
            query_params.append(f"%{name}%")
        if year:
            query += " AND year LIKE ?"
            query_params.append(year)  # exact year
        if author:
            query += " AND author LIKE ?"
            query_params.append(f"%{author}%")

        search_results = self.__cur.execute(query, query_params).fetchall()
        books_list = [Models.Book(**book_data) for book_data in search_results]
        return books_list

    def delete_book(self, book_id: int) -> None:
        """
        - Удаление книги: Пользователь может удалить книгу из базы по заданным параметрам.

        Deletes book from database

        :param book_id: id of book to delete
        :return: None
        """

        query = "DELETE FROM books WHERE id = ?"
        self.__cur.execute(query, (book_id, ))
        self.__db.commit()

    def edit_book(self, book_id: int, **kwargs) -> Models.Book:
        """
        - Редактирование данных о книге: Пользователь может изменить данные о книге в базе.

        Edits book genral information

        :param book_id: id of book to edit
        :param kwargs: new information: name, author, year
        :raises ValueError if book id was not found
        :return: new instance of Models.Book of edited book
        """

        query = "SELECT id, name, author, year FROM books WHERE id = ?"  # get actual info about book
        search_results = self.__cur.execute(query, (book_id, )).fetchone()

        if not search_results:
            raise ValueError("No such id in database")

        # create Book model from actual info
        actual_info = Models.Book(**search_results)

        # or use search_results[0], search_results[1], search_results[2]
        name = kwargs.get("name", actual_info.name)  # if name not passed - take current
        author = kwargs.get("author", actual_info.author)  # if author not passed - take current
        year = kwargs.get("year", actual_info.year)  # if year not passed - take current

        query = "UPDATE books SET name = ?, author = ?, year = ? WHERE id = ?"  # edit
        self.__cur.execute(query, (name, author, year, book_id)).fetchone()
        self.__db.commit()

        return Models.Book(
            id=book_id,
            name=name,
            author=author,
            year=year
        )

    def get_all_books(self) -> list[Models.Book] or []:
        """
        - Вывод списка всех книг: Выводит список всех книг в базе.

        Returns list of all books in database

        :return: list of [Models.Book] or empty list
        """

        query = "SELECT id, name, author, year FROM books"
        search_results = self.__cur.execute(query).fetchall()
        books_list = [Models.Book(**book_data) for book_data in search_results]
        return books_list
